from rest_framework import serializers
from user.models import User, Operation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'balance']


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['currentBalance', 'oldBalance', 'difference', 'created_at']
