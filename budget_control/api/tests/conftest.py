import pytest

from datetime import date
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
def api_client_auth(api_client, user):
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture()
def user():
    return baker.make("User")


@pytest.fixture()
def mock_incomes(mock_date):
    return baker.make("Income", 2, date=mock_date)


@pytest.fixture()
def mock_expenses(mock_food_expenses, mock_health_expenses):
    return mock_food_expenses + mock_health_expenses


@pytest.fixture()
def mock_food_expenses(mock_date):
    return baker.make("Expense", 2, date=mock_date, category="food")


@pytest.fixture()
def mock_health_expenses(mock_date):
    return baker.make("Expense", 2, date=mock_date, category="health")


@pytest.fixture()
def mock_date():
    return date(2023, 5, 14)
