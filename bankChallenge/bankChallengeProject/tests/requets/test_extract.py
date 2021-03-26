import pytz
from rest_framework import status
from rest_framework.test import APITestCase

from tests.mock_data import JsonObjects
from user.models import User, Operation
from datetime import datetime
from mock import patch


class ExtractRequestTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(ExtractRequestTest, cls).setUpClass()

        user_data = JsonObjects.user('tom')
        cls.user = User.objects.create(**user_data)
        cls.user.save()

        transaction_data_1 = JsonObjects.transaction(cls.user, 'Buy a book', -30)
        transaction_data_2 = JsonObjects.transaction(cls.user, 'Payment receive', 500)
        transaction_data_3 = JsonObjects.transaction(cls.user, 'Buy some snacks', -40)
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2021, 3, 10, tzinfo=pytz.UTC)
            cls.transaction_1 = Operation.objects.create(**transaction_data_1)
            cls.transaction_1.save()
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2021, 3, 11, tzinfo=pytz.UTC)
            cls.transaction_2 = Operation.objects.create(**transaction_data_2)
            cls.transaction_2.save()
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2021, 3, 15, tzinfo=pytz.UTC)
            cls.transaction_3 = Operation.objects.create(**transaction_data_3)
            cls.transaction_3.save()

        cls.endpoint = '/user/%s/extract' % cls.user.id

    @classmethod
    def tearDownClass(cls):
        super(ExtractRequestTest, cls).tearDownClass()
        cls.transaction_1.delete()
        cls.transaction_2.delete()
        cls.transaction_3.delete()
        cls.user.delete()

    def test_check_extract__all__status200(self):
        # Arrange
        # Act
        resp = self.client.get(self.endpoint)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 3)

    def test_check_extract__debit__status200(self):
        # Arrange
        filter_data = '?transaction_type=debit'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 2)

    def test_check_extract__credit__status200(self):
        # Arrange
        filter_data = '?transaction_type=credit'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 1)

    def test_check_extract__credit_uppercase__status200(self):
        # Arrange
        filter_data = '?transaction_type=CREDIT'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 1)

    def test_check_extract__from_date__status200(self):
        # Arrange
        filter_data = '?start_date=2021-03-11T00:00Z'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 2)

    def test_check_extract__to_date__status200(self):
        # Arrange
        filter_data = '?end_date=2021-03-11T00:00Z'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 2)

    def test_check_extract__between_dates__status200(self):
        # Arrange
        filter_data = '?start_date=2021-03-11T00:00Z&end_date=2021-03-13T00:00Z'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 1)

    def test_check_extract__between_dates_exact__status200(self):
        # Arrange
        filter_data = '?start_date=2021-03-10T00:00Z&end_date=2021-03-11T00:00Z'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 2)

    def test_check_extract__invalid_date__status404(self):
        # Arrange
        filter_data = '?start_date=2021-03-32T00:00Z'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.data['detail'], 'The date is invalid.')

    def test_check_extract__invalid_user__status404(self):
        # Arrange
        endpoint = '/user/9999/extract'
        # Act
        resp = self.client.get(endpoint)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(resp.data['detail'], 'User not found.')

    def test_check_extract__invalid_type__status200(self):
        # Arrange
        filter_data = '?transaction_type=wrongType'
        # Act
        resp = self.client.get(self.endpoint + filter_data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['count'], 0)
