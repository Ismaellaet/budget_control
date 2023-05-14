import pytest

from datetime import date
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
def mock_incomes():
    return baker.make("Income", 2, date=date(2023, 5, 14))


@pytest.fixture()
def mock_expenses():
    return baker.make("Expense", 2, date=date(2023, 5, 14))
