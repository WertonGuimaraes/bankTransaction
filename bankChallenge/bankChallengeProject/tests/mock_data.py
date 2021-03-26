from datetime import datetime


class JsonObjects(object):

    @staticmethod
    def user(username):
        return {'username': username}

    @staticmethod
    def transaction(user, description, value):
        return {
            'user': user,
            'description': description,
            'current_balance': user.balance + value,
            'old_balance': user.balance,
            'value': value,
            'transaction_type': 'debit' if value < 0 else 'credit'
        }
