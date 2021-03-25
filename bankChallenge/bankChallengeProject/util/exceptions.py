from rest_framework.exceptions import APIException
from rest_framework import status


class BalanceError(APIException):
    def __init__(self):
        detail = "You don\'t have money."
        super(BalanceError, self).__init__(detail)
        self.status_code = status.HTTP_403_FORBIDDEN


class TransactionBodyError(APIException):
    def __init__(self):
        detail = "value is required field."
        super(TransactionBodyError, self).__init__(detail)
        self.status_code = status.HTTP_400_BAD_REQUEST


class TransactionTypeError(APIException):
    def __init__(self):
        detail = "TypeError: value needs to be a int or a float."
        super(TransactionTypeError, self).__init__(detail)
        self.status_code = status.HTTP_400_BAD_REQUEST


class UserNotFound(APIException):
    def __init__(self):
        detail = "User not found."
        super(UserNotFound, self).__init__(detail)
        self.status_code = status.HTTP_404_NOT_FOUND


class InvalidDateError(APIException):
    def __init__(self):
        detail = "The date is invalid."
        super(InvalidDateError, self).__init__(detail)
        self.status_code = status.HTTP_400_BAD_REQUEST








