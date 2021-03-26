import pytz
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from user.serializers import UserSerializer, OperationSerializer
from user.models import User, Operation
from util.transaction import Transaction
from util.validator import validate_user, validate_value, validate_date, validate_required_fields
from datetime import datetime


class OperationView(APIView):
    def post(self, request, user_id):
        # the validator was created. But, we can check the fields using serializer `.is_valid`
        user = validate_user(user_id)
        value = validate_value(request)
        description = validate_required_fields(request, 'description')

        user_transaction = Transaction(user)
        updated_user_after_transaction = user_transaction.make_transaction(value, description)
        updated_user_after_transaction = UserSerializer(updated_user_after_transaction)
        return Response(updated_user_after_transaction.data)


class ExtractView(generics.ListAPIView):
    serializer_class = OperationSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id'] if 'user_id' in self.kwargs else -1
        transaction_type = self.request.query_params.get('transaction_type', 'debit,credit').split(',')
        start_date = self.request.query_params.get('start_date', datetime.min)
        end_date = self.request.query_params.get('end_date', datetime.now(tz=pytz.UTC))

        validate_user(user_id)
        validate_date(start_date)
        transaction_type = [_type.lower() for _type in transaction_type]

        return Operation.objects.filter(user=user_id, transaction_type__in=transaction_type,
                                        created_at__range=(start_date, end_date))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
