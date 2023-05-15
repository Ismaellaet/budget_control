import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestSummaryViewSet:
    def test_get_summary(self, api_client_auth, mock_food_expenses, mock_health_expenses, mock_incomes, mock_date):
        url = reverse(
            "summary-get-summary", args=[mock_date.year, f"0{mock_date.month}"]
        )
        response = api_client_auth.get(url)
        assert response.status_code == status.HTTP_200_OK

        total_income = sum([income.value for income in mock_incomes])
        total_expense = sum([expense.value for expense in mock_health_expenses + mock_food_expenses])
        total_spent_by_category = {
            "food": str(sum([expense.value for expense in mock_food_expenses])),
            "health": str(sum([expense.value for expense in mock_health_expenses])),
        }

        assert response.data["total_income"] == str(total_income)
        assert response.data["total_expense"] == str(total_expense)
        assert response.data["total_spent_by_category"] == total_spent_by_category
        assert response.data["balance"] == str(total_income - total_expense)

    def test_get_summary_invalid_month(self, api_client_auth, mock_date, mock_expenses):
        url = reverse(
            "summary-get-summary",
            args=[mock_date.year, f"0{mock_date.month + 1}"]
        )
        response = api_client_auth.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_summary_invalid_year(self, api_client_auth, mock_date, mock_expenses):
        url = reverse(
            "summary-get-summary",
            args=[mock_date.year + 1, f"0{mock_date.month}"]
        )
        response = api_client_auth.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
