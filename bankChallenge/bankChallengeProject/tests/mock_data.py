from datetime import datetime


class JsonObjects(object):

    @staticmethod
    def user(username, balance=0):
        return {'username': username, 'balance': balance}

    @staticmethod
    def transaction(user, description, current_balance=100, old_balance=150, created_at=datetime.now()):
        return {
            'user': user,
            'description': description,
            'current_balance': current_balance,
            'old_balance': old_balance,
            'difference': current_balance-old_balance,
            'transaction_type': 'debit' if current_balance > old_balance else 'credit',
            'created_at': created_at
        }
