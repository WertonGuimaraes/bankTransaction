from datetime import datetime
from user.models import User
from util.exceptions import TransactionBodyError, TransactionTypeError, UserNotFound, InvalidDateError


def validate_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise UserNotFound()


def validate_value(request):
    if 'value' in request.data.keys():
        try:
            return float(request.data['value'])
        except ValueError:
            raise TransactionTypeError()
    raise TransactionBodyError()


def validate_date(date):
    try:
        if type(date) == str:
            datetime.fromisoformat(date.replace('Z', '+00:00'))
    except ValueError:
        raise InvalidDateError()
