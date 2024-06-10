from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from networth_tracker.api.serializers import AccountSerializer, BankAccountSerializer
from networth_tracker.models import Account, BankAccount


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class BankAccountViewSet(ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class UserBankAccountViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
