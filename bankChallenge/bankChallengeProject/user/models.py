from django.db import models


class User(models.Model):
    username = models.CharField(max_length=254, null=False, blank=False)
    balance = models.FloatField(default=0)  # TODO: Tem que ser logico e atualizar teste do models
    created_at = models.DateTimeField('Created Time', auto_now_add=True)


class Operation(models.Model):
    user = models.ForeignKey(User, related_name='operations', on_delete=models.CASCADE)
    description = models.CharField(max_length=254, null=False, blank=False)
    current_balance = models.IntegerField()
    old_balance = models.IntegerField()
    difference = models.IntegerField()
    transaction_type = models.CharField(max_length=254, null=False, blank=False)
    created_at = models.DateTimeField('Created Time', auto_now_add=True)
