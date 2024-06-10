# networth_tracker/tests.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

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
        url = reverse("register")

        data = {
            "email": "normal@user.com",
            "password": "foo",
        }

        client = APIClient()
        response = client.post(url, data, format="json")

        assert response.status_code == 200
        assert response.data["email"] == "normal@user.com"
        assert get_user_model().objects.filter(email="normal@user.com").exists()
