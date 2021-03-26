from django.test import TestCase

from tests.mock_data import JsonObjects
from user.models import User, Operation


class ModelUserTest(TestCase):
    def test__create_user(self):
        # Arrange
        user_data = JsonObjects.user('tom')
        # Act
        user_created = User.objects.create(**user_data)
        # Assert
        self.assertEqual(user_created.id, 1)
        self.assertEqual(user_created.username, 'tom')
        self.assertEqual(user_created.balance, 0)


class ModelOperationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(**JsonObjects.user('tom'))

    def test__create_transaction(self):
        # Arrange
        transaction_data = JsonObjects.transaction(self.user, 'Buy a book', -10)
        # Act
        transaction_created = Operation.objects.create(**transaction_data)
        # Assert
        self.assertEqual(transaction_created.id, 1)
        self.assertEqual(transaction_created.user, self.user)
        self.assertEqual(transaction_created.description, 'Buy a book')
