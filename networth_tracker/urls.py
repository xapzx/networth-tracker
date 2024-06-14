from django.urls import include, path
from rest_framework import routers

from .api.viewsets import AccountViewSet, AdminBankAccountViewSet, BankAccountViewSet
from .apis import RegisterView

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"bank_accounts", BankAccountViewSet, basename="bank-accounts")
router.register(r"admin_bank_accounts", AdminBankAccountViewSet, basename="admin-bank-accounts")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]
