import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from networth_tracker.tests.factories import (
    AccountFactory,
    BankAccountFactory,
    CustomUserFactory,
    EtfFactory,
    EtfTransactionFactory,
    SuperannuationFactory,
)

register(CustomUserFactory)
register(CustomUserFactory, "custom_user_1")

register(BankAccountFactory)
register(BankAccountFactory, "bank_account_1")
register(BankAccountFactory, "bank_account_2")

register(AccountFactory)
register(AccountFactory, "account_1")

register(EtfFactory)
register(EtfFactory, "etf_1")
register(EtfFactory, "etf_2")

register(EtfTransactionFactory)
register(EtfTransactionFactory, "etf_transaction_1")

register(SuperannuationFactory)
register(SuperannuationFactory, "superannuation_1")


@pytest.fixture(scope="session")
def create_auth_client():
    def _create_auth_client(user):
        client = APIClient()
        client.force_login(user)
        return client

    return _create_auth_client


@pytest.fixture
def admin_user(custom_user_factory):
    return custom_user_factory(is_staff=True)
