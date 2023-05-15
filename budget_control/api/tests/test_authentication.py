import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestAuthentication:
    def test_authenticated_user_can_access_resources(self, api_client, user):
        token = AccessToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = api_client.get(reverse("income-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_user_cannot_access_resources(self, api_client):
        response = api_client.get(reverse("income-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
