import pytest

from datetime import datetime, date
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from ...models import Expense


@pytest.fixture()
def expense_data():
    return {
        "description": "Expense Test",
        "value": "100.50",
        "date": "2023-05-14"
    }


@pytest.mark.django_db
class TestExpenseViewSet:
    def test_list_expenses(self, api_client, mock_expenses):
        response = api_client.get(reverse("expense-list"))

        assert len(response.data) == len(mock_expenses)
        assert response.status_code == status.HTTP_200_OK

    def test_create_valid_expense(self, api_client, expense_data):
        response = api_client.post(path=reverse("expense-list"), data=expense_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == expense_data["description"]
        assert response.data["value"] == expense_data["value"]
        assert response.data["date"] == expense_data["date"]

    def test_retrieve_expense(self, api_client):
        expense = baker.make("Expense")
        response = api_client.get(
            reverse("expense-detail", args=[expense.id])
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == expense.description
        assert response.data["value"] == str(expense.value)
        assert response.data["date"] == str(expense.date)

    def test_update_expense(self, api_client):
        expense = baker.make("Expense")
        url = reverse("expense-detail", args=[expense.id])
        response = api_client.put(path=url, data={
            "description": "Updated Expense",
            "value": "99.99",
            "date": "2022-02-27",
        })
        expense.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == expense.description
        assert response.data["value"] == str(expense.value)
        assert response.data["date"] == str(expense.date)

    def test_delete_expense(self, api_client):
        expense = baker.make("Expense")
        url = reverse("expense-detail", args=[expense.id])
        response = api_client.delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Expense.objects.filter(id=expense.id).exists()

    def test_get_expenses_by_year_month(self, api_client, mock_expenses):
        year, month = 2022, 3
        baker.make("Expense", 2, date=date(year, month, 10))
        url = reverse("expense-by-year-month", args=[year, f"0{month}"])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        for expense in response.json():
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            assert expense not in mock_expenses
            assert expense_date.year == year
            assert expense_date.month == month
