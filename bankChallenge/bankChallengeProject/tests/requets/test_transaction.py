from rest_framework import status
from rest_framework.test import APITestCase
from tests.mock_data import JsonObjects
from user.models import User, Operation


class OperationRequestTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(**JsonObjects.user('tom', 100))
        self.user.save()
        self.endpoint = '/user/%s/action' % self.user.id

    def tearDown(self):
        self.user.delete()

    def test_create_transaction__credit_int_value__status200(self):
        # Arrange
        data = {'value': 1}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 101)

    def test_create_transaction__credit_float_value__status200(self):
        # Arrange
        data = {'value': 1.05}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 101.05)

    def test_create_transaction__debit__status200(self):
        # Arrange
        data = {'value': -1}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 99)

    def test_create_transaction__debit_all_money__status200(self):
        # Arrange
        data = {'value': -100}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 0)

    def test_create_transaction__debit_no_limit__status403(self):
        # Arrange
        data = {'value': -100.01}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(resp.data['detail'], 'You don\'t have money.')
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 100)

    def test_create_transaction__without_value_attr__status400(self):
        # Arrange
        data = {}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.data['detail'], 'value is required field.')
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 100)

    def test_create_transaction__with_wrong_value__status400(self):
        # Arrange
        data = {'value': 'a'}
        # Act
        resp = self.client.post(self.endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.data['detail'], 'TypeError: value needs to be a int or a float.')
        self.assertEquals(User.objects.get(pk=self.user.pk).balance, 100)

    def test_create_transaction__wrong_user__status404(self):
        # Arrange
        data = {'value': 100}
        endpoint = '/user/9999/action'
        # Act
        resp = self.client.post(endpoint, data)
        # Assert
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(resp.data['detail'], 'User not found.')



