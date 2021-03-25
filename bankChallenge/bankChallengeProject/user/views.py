from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from user.serializers import UserSerializer, OperationSerializer
from user.models import User, Operation
from util.transaction import Transaction
from util.validator import validate_user, validate_value
from datetime import datetime


class OperationView(APIView):
    def post(self, request, user_id):
        user = validate_user(user_id)
        value = validate_value(request)

        user_transaction = Transaction(user)
        updated_user_after_transaction = user_transaction.make_transaction(value)
        updated_user_after_transaction = UserSerializer(updated_user_after_transaction)
        return Response(updated_user_after_transaction.data)


class ExtractView(generics.ListAPIView):
    serializer_class = OperationSerializer

    def get_queryset(self):
        # date example: 2021-03-25T03:47:10.309474Z
        user_id = self.kwargs['user_id'] if 'user_id' in self.kwargs else -1
        transaction_type = self.request.query_params.get('transactionType', 'debit,credit').split(',')
        start_date = self.request.query_params.get('startDate', datetime.min)
        end_date = self.request.query_params.get('endDate', datetime.now())

        validate_user(user_id)

        return Operation.objects.filter(user=user_id, transactionType__in=transaction_type,
                                        created_at__range=(start_date, end_date))


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get']
