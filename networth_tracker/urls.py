# networth_tracker/urls.py

from django.urls import include, path
from rest_framework import routers

from .api.viewsets import AccountViewSet, BankAccountViewSet, EtfTransactionViewSet, EtfViewSet
from .apis import RegisterView

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"bank_accounts", BankAccountViewSet, basename="bank-accounts")
router.register(r"etfs", EtfViewSet, basename="etfs")
router.register(r"etf_transactions", EtfTransactionViewSet, basename="etf-transactions")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]
