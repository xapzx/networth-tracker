from rest_framework.viewsets import ModelViewSet

from networth_tracker.api.serializers import AccountSerializer, BankAccountSerializer
from networth_tracker.models import Account, BankAccount


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class BankAccountViewSet(ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
