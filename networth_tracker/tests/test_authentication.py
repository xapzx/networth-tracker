# networth_tracker/tests/test_authentication.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from networth_tracker.models import CustomUser

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_call_with_token_authentication():
    username = "test-user"
    password = "foobar"
    CustomUser.objects.create_user(username, password=password)

    client = APIClient()
    token_url = reverse("api_token_auth")

    data = {"username": username, "password": password}

    token_response = client.post(token_url, data, format="json")
    token = token_response.data["token"]

    url = reverse("bank-accounts-list")
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
