import pytest

from datetime import datetime, date
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from ...models import Income


@pytest.fixture()
def income_data():
    return {
        "description": "Income Test",
        "value": "100.50",
        "date": "2023-05-14"
    }


@pytest.mark.django_db
class TestIncomeViewSet:

    def test_list_incomes(self, api_client_auth, mock_incomes):
        response = api_client_auth.get(reverse("income-list"))

        assert response.status_code == status.HTTP_200_OK

    def test_create_valid_income(self, api_client_auth, income_data):
        response = api_client_auth.post(path=reverse("income-list"), data=income_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == income_data["description"]
        assert response.data["value"] == income_data["value"]
        assert response.data["date"] == income_data["date"]

    def test_retrieve_income(self, api_client_auth):
        income = baker.make("Income")
        response = api_client_auth.get(reverse("income-detail", args=[income.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == income.description
        assert response.data["value"] == str(income.value)
        assert response.data["date"] == str(income.date)

    def test_update_income(self, api_client_auth):
        income = baker.make("Income")
        url = reverse("income-detail", args=[income.id])
        response = api_client_auth.put(path=url, data={
            "description": "Updated Income",
            "value": "99.99",
            "date": "2022-02-27",
        })
        income.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == income.description
        assert response.data["value"] == str(income.value)
        assert response.data["date"] == str(income.date)

    def test_delete_income(self, api_client_auth):
        income = baker.make("Income")
        url = reverse("income-detail", args=[income.id])
        response = api_client_auth.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Income.objects.filter(id=income.id).exists()

    def test_get_incomes_by_year_month(self, api_client_auth, mock_incomes):
        year, month = 2022, 3
        baker.make("Income", 2, date=date(year, month, 10))
        url = reverse("income-by-year-month", args=[year, f"0{month}"])
        response = api_client_auth.get(url)

        assert response.status_code == status.HTTP_200_OK
        for income in response.json():
            income_date = datetime.strptime(income["date"], "%Y-%m-%d")
            assert income not in mock_incomes
            assert income_date.year == year
            assert income_date.month == month
