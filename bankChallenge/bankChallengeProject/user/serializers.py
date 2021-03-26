from rest_framework import serializers
from user.models import User, Operation


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'balance']


class OperationSerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length=254, required=True)

    class Meta:
        model = Operation
        fields = ['description', 'current_balance', 'old_balance', 'value', 'created_at']
