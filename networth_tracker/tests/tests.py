# networth_tracker/tests.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from networth_tracker.api.serializers import BankAccountSerializer
from networth_tracker.models import BankAccount

pytestmark = pytest.mark.django_db


class TestUsersManagers:

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")

        assert user.email == "normal@user.com"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            assert user.username is None
        except AttributeError:
            pass

        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(TypeError):
            User.objects.create_user(email="")
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")

        assert admin_user.email == "super@user.com"
        assert admin_user.is_active is True
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            assert admin_user.username is None
        except AttributeError:
            pass

        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


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
