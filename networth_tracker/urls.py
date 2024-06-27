# networth_tracker/urls.py

from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from networth_tracker.api.viewsets import (
    AccountViewSet,
    BankAccountViewSet,
    EtfTransactionViewSet,
    EtfViewSet,
    SuperannuationViewSet,
)
from networth_tracker.apis import RegisterView

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"bank_accounts", BankAccountViewSet, basename="bank-accounts")
router.register(r"etfs", EtfViewSet, basename="etfs")
router.register(r"etf_transactions", EtfTransactionViewSet, basename="etf-transactions")
router.register(r"superannuations", SuperannuationViewSet, basename="superannuations")

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]
