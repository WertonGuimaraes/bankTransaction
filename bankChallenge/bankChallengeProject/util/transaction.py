from user.models import Operation

from util.exceptions import BalanceError


class Transaction:

    def __init__(self, user):
        self.user = user

    def _register_operation(self, value):
        transaction_type = 'credit' if value >= 0 else 'debit'
        new_balance = self.user.balance + value

        if new_balance < 0:
            raise BalanceError()

        operation = Operation(currentBalance=new_balance,
                              oldBalance=self.user.balance,
                              difference=value,
                              transactionType=transaction_type)
        operation.user = self.user
        operation.save()
        return operation

    def make_transaction(self, value):
        if value != 0:
            operation_result = self._register_operation(value)
            self.user.balance = operation_result.currentBalance
            self.user.save()
        return self.user
