from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from networth_tracker.api.permissions import AccountOwnerOnly, BankAccountOwnerOnly
from networth_tracker.api.serializers import AccountSerializer, BankAccountSerializer
from networth_tracker.models import Account, BankAccount


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, AccountOwnerOnly]


class AdminBankAccountViewSet(ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class BankAccountViewSet(ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, BankAccountOwnerOnly]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
