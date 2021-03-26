from user.models import Operation

from util.exceptions import BalanceError


class Transaction:

    def __init__(self, user):
        self.user = user

    def _register_operation(self, value, description):
        transaction_type = 'credit' if value >= 0 else 'debit'
        new_balance = self.user.balance + value

        if new_balance < 0:
            raise BalanceError()

        operation = Operation(current_balance=new_balance,
                              old_balance=self.user.balance,
                              value=value,
                              transaction_type=transaction_type,
                              description=description)
        operation.user = self.user
        operation.save()
        return operation

    def make_transaction(self, value, description):
        if value != 0:
            self._register_operation(value, description)
        return self.user
