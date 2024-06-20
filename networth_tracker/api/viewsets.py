from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from networth_tracker.api.permissions import isOwnerOrSuperuser
from networth_tracker.api.serializers import (
    AccountSerializer,
    BankAccountSerializer,
    EtfSerializer,
    EtfTransactionSerializer,
)
from networth_tracker.models import Account, BankAccount, Etf, EtfTransaction


class AccountViewSet(ModelViewSet):
    """
    API endpoint for managing user-owned `Account`.

    Permissions:
        - Requires authentication.
        - Only the owner or a superuser can view, modify or delete accounts.

    Actions:

        - List (GET /accounts): Retrieves all accounts belonging to the user.
        - Create (POST /accounts): Creates a new account for the user.
        - Retrieve (GET /accounts/<pk>): Retrieves a specific account by its ID.
        - Update (PUT /accounts/<pk>): Updates an existing account for the user.
        - Partial Update (PATCH /accounts/<pk>): Partially updates an existing account for the user
        - Delete (DELETE /accounts/<pk>): Deletes a specific account by its ID.
    """

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AccountSerializer
        return super().get_serializer_class()

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, isOwnerOrSuperuser]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdminBankAccountViewSet(ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser]


class BankAccountViewSet(ModelViewSet):
    """
    API endpoint for managing user-owned `BankAccount`.

    Permissions:
        - Requires authentication.
        - Only the owner or a superuser can view, modify or delete bank accounts.

    Actions:

        - List (GET /bank_accounts): Retrieves all bank accounts belonging to the user.
        - Create (POST /bank_accounts): Creates a new bank account for the user.
        - Retrieve (GET /bank_accounts/<pk>): Retrieves a specific bank account by its ID.
        - Update (PUT /bank_accounts/<pk>): Updates an existing bank account for the user.
        - Delete (DELETE /bank_accounts/<pk>): Deletes a bank account owned by the user.
    """

    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, isOwnerOrSuperuser]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EtfViewSet(ModelViewSet):
    """
    API endpoint for managing user-owned `Etf`.

    Permissions:
        - Requires authentication (`IsAuthenticated`).
        - Only the owner or a superuser can view, modify or delete ETFs (`isOwnerOrSuperuser`).

    Actions:

        - List (GET /etfs): Retrieves all ETFs belonging to the authenticated user.
        - Create (POST /etfs): Creates a new ETF for the authenticated user.
        - Retrieve (GET /etfs/<pk>): Retrieves a specific ETF by its ID.
        - Update (PUT /etfs/<pk>): Updates an existing ETF for the authenticated user.
        - Delete (DELETE /etfs/<pk>): Deletes an ETF owned by the authenticated user.

    Nested transactions endpoint:

        - GET /etfs/<pk>/transactions: Retrieves all transactions associated with a specific ETF
            - Requires the ETF to belong to the authenticated user.
    """

    queryset = Etf.objects.all()
    serializer_class = EtfSerializer
    permission_classes = [IsAuthenticated, isOwnerOrSuperuser]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, units_held=0, average_cost=0)

    @action(detail=True, methods=["get"], url_path="transactions")
    def get_etf_transactions(self, request, pk=None):
        queryset = EtfTransaction.objects.filter(etf__user=self.request.user)

        if pk:
            queryset = queryset.filter(etf=pk)

        serializer = EtfTransactionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EtfTransactionViewSet(ModelViewSet):
    """
    API endpoint for managing user-owned `EtfTransaction`.

    Permissions:
        - Requires authentication (`IsAuthenticated`).
        - Only the owner or a superuser can view, modify or delete ETF transactions
          (`isOwnerOrSuperuser`).

    Actions:

        - List (GET /etf_transactions): Retrieves all transactions for the current user
        - Create (POST /etf_transactions): Creates a new transaction for the current user
        - Retrieve (GET /etf_transactions/<pk>): Retrieves a specific transaction by its ID
        - Update (PUT /etf_transactions/<pk>): Updates an existing transaction for the current user
        - Delete (DELETE /etf_transactions/<pk>): Deletes a transaction owned by the current user
    """

    queryset = EtfTransaction.objects.all()
    serializer_class = EtfTransactionSerializer
    permission_classes = [IsAuthenticated, isOwnerOrSuperuser]

    def get_queryset(self):
        return self.queryset.filter(etf__user=self.request.user)
