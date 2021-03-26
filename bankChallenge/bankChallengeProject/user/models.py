from django.db import models


class User(models.Model):
    username = models.CharField(max_length=254, null=False, blank=False)
    created_at = models.DateTimeField('Created Time', auto_now_add=True)

    def _get_balance(self):
        all_operations = self.operations.all()
        return all_operations.last().current_balance if self.operations.exists() > 0 else 0
    balance = property(_get_balance)


class Operation(models.Model):
    user = models.ForeignKey(User, related_name='operations', on_delete=models.CASCADE)
    description = models.CharField(max_length=254, null=False, blank=False)
    current_balance = models.FloatField()
    old_balance = models.FloatField()
    value = models.FloatField()
    transaction_type = models.CharField(max_length=254, null=False, blank=False)
    created_at = models.DateTimeField('Created Time', auto_now_add=True)
