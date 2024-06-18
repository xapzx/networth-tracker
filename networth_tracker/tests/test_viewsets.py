# networth_tracker/test_viewsets.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from networth_tracker.api.serializers import BankAccountSerializer
from networth_tracker.models import Account, BankAccount

pytestmark = pytest.mark.django_db


class TestRegisterView:
    def test_user_registered(self):
        data = {
            "email": "normal@user.com",
            "password": "foo",
        }

        client = APIClient()

        url = reverse("register")
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "normal@user.com"
        assert get_user_model().objects.filter(email="normal@user.com").exists()


class TestUserBankAccountViewSet:
    def test_get_user_bank_accounts(
        self,
        create_auth_client,
        custom_user_1,
        custom_user_factory,
        bank_account_1,
        bank_account_factory,
    ):
        another_user_account = bank_account_factory(
            user=custom_user_factory(email="anotheruser@user.com"),
        )

        url = reverse("bank-accounts-list")
        client = create_auth_client(custom_user_1)
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert BankAccountSerializer(bank_account_1).data in response.data
        assert BankAccountSerializer(another_user_account).data not in response.data

    def test_unauthenticated(self):
        client = APIClient()

        url = reverse("bank-accounts-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_bank_account_by_id(self, create_auth_client, custom_user_1, bank_account_1):
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        client = create_auth_client(custom_user_1)
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert BankAccountSerializer(bank_account_1).data == response.data

    def test_get_bank_account_by_id_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, bank_account_1
    ):
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_bank_account_is_deleted(self, create_auth_client, custom_user_1, bank_account_1):
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        client = create_auth_client(custom_user_1)
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BankAccount.objects.filter(id=bank_account_1.id).exists()

    def test_delete_bank_account_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, bank_account_1
    ):
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        response = client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert BankAccount.objects.filter(id=bank_account_1.id).exists()

    def test_bank_account_is_partial_updated(
        self, create_auth_client, custom_user_1, bank_account_1
    ):
        client = create_auth_client(custom_user_1)
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        data = {"balance": 20000.0}
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert BankAccount.objects.get(id=bank_account_1.id).balance == 20000.0

    def test_partial_update_bank_account_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, bank_account_1
    ):
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        data = {"balance": 20000.0}
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_bank_account_is_updated(self, create_auth_client, custom_user_1, bank_account_1):
        client = create_auth_client(custom_user_1)
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        data = {
            "bank": "Commonwealth Bank",
            "account_name": "Complete Access",
            "balance": 20000.0,
            "interest_rate": 0.0,
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert BankAccount.objects.get(id=bank_account_1.id).balance == 20000.0

    def test_bank_account_update_incomplete_request(
        self, create_auth_client, custom_user_1, bank_account_1
    ):
        client = create_auth_client(custom_user_1)
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        data = {
            "bank": "Commonwealth Bank",
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_bank_account_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, bank_account_1
    ):
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        url = reverse("bank-accounts-detail", kwargs={"pk": bank_account_1.id})
        data = {
            "bank": "Commonwealth Bank",
            "account_name": "Complete Access",
            "balance": 20000.0,
            "interest_rate": 0.0,
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_create_bank_account(self, create_auth_client, custom_user_1):
        client = create_auth_client(custom_user_1)
        url = reverse("bank-accounts-list")
        data = {
            "bank": "Commonwealth Bank",
            "account_name": "Complete Access",
            "balance": 20000.0,
            "interest_rate": 0.0,
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert BankAccount.objects.filter(user=custom_user_1).exists()


class TestAccountViewSet:
    def test_account_is_created(self, create_auth_client, custom_user_1):
        client = create_auth_client(custom_user_1)
        url = reverse("accounts-list")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "salary": 10000.0,
            "eoy_cash_goal": 20000.0,
            "emergency_fund": 5000.0,
            "allocation_intensity": 1,
            "allocation_etfs": 0.0,
            "allocation_stocks": 0.0,
            "allocation_cryptocurrency": 0.0,
            "allocation_cash": 0.0,
            "allocation_managed_funds": 0.0,
            "allocation_other": 0.0,
            "short_term_tax_rate": 0.0,
            "long_term_tax_rate": 0.0,
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Account.objects.filter(user=custom_user_1).exists()

    def test_get_account_list_for_user(
        self, create_auth_client, custom_user_1, account_1, custom_user_factory, account_factory
    ):
        account_factory(
            user=custom_user_factory(email="anotheruser@user.com"),
        )

        client = create_auth_client(custom_user_1)
        url = reverse("accounts-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == account_1.id

    def test_get_account_by_id(self, create_auth_client, custom_user_1, account_1):
        client = create_auth_client(custom_user_1)
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == account_1.id

    def test_get_account_by_id_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, account_1
    ):
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_account_by_id(self, create_auth_client, custom_user_1, account_1):
        client = create_auth_client(custom_user_1)
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Account.objects.filter(id=account_1.id).exists()

    def test_update_account_by_id(self, create_auth_client, custom_user_1, account_1):
        client = create_auth_client(custom_user_1)
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "salary": 10000.0,
            "eoy_cash_goal": 20000.0,
            "emergency_fund": 5000.0,
            "allocation_intensity": 1,
            "allocation_etfs": 0.0,
            "allocation_stocks": 0.0,
            "allocation_cryptocurrency": 0.0,
            "allocation_cash": 0.0,
            "allocation_managed_funds": 0.0,
            "allocation_other": 0.0,
            "short_term_tax_rate": 0.0,
            "long_term_tax_rate": 0.0,
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert Account.objects.filter(id=account_1.id).exists()

    def test_update_account_by_id_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, account_1
    ):
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "salary": 10000.0,
            "eoy_cash_goal": 20000.0,
            "emergency_fund": 5000.0,
            "allocation_intensity": 1,
            "allocation_etfs": 0.0,
            "allocation_stocks": 0.0,
            "allocation_cryptocurrency": 0.0,
            "allocation_cash": 0.0,
            "allocation_managed_funds": 0.0,
            "allocation_other": 0.0,
            "short_term_tax_rate": 0.0,
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_account_incomplete_data(self, create_auth_client, custom_user_1, account_1):
        client = create_auth_client(custom_user_1)
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        data = {
            "first_name": "John",
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_partially_update_account_by_id(self, create_auth_client, custom_user_1, account_1):
        client = create_auth_client(custom_user_1)
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        data = {
            "first_name": "John",
        }
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == data["first_name"]

    def test_partially_update_account_by_id_restricted_if_not_owner(
        self, create_auth_client, custom_user_factory, account_1
    ):
        client = create_auth_client(custom_user_factory(email="anotheruser@user.com"))
        url = reverse("accounts-detail", kwargs={"pk": account_1.id})
        data = {
            "first_name": "John",
        }
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
