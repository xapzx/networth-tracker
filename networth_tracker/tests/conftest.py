import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from networth_tracker.tests.factories import AccountFactory, BankAccountFactory, CustomUserFactory

register(CustomUserFactory)
register(CustomUserFactory, "custom_user_1")

register(BankAccountFactory)
register(BankAccountFactory, "bank_account_1")
register(BankAccountFactory, "bank_account_2")

register(AccountFactory)
register(AccountFactory, "account_1")


@pytest.fixture(scope="session")
def create_auth_client():
    def _create_auth_client(user):
        client = APIClient()
        client.force_login(user)
        return client

    return _create_auth_client
