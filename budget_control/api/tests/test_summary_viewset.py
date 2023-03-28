from datetime import datetime

from django.urls import reverse

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class SummaryViewSetTestCase(APITestCase):
    def setUp(self):
        self.date = datetime.now()
        self.year = self.date.year
        self.month = f"{self.date:%m}"
        self.incomes = baker.make("Income", 2)
        self.expenses1 = baker.make("Expense", 2, category="food", date=self.date)
        self.expenses2 = baker.make("Expense", 2, category="health", date=self.date)
        self.expenses = self.expenses1 + self.expenses2

    def test_get_summary(self):
        url = reverse(
            "summary-get-summary", kwargs={"year": self.year, "month": self.month}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        total_income = sum([income.value for income in self.incomes])
        total_expense = sum([expense.value for expense in self.expenses])
        total_spent_by_category = {
            "food": str(sum([expense.value for expense in self.expenses1])),
            "health": str(sum([expense.value for expense in self.expenses2])),
        }

        self.assertEqual(response.data["total_income"], str(total_income))
        self.assertEqual(response.data["total_expense"], str(total_expense))
        self.assertEqual(response.data["total_spent_by_category"], total_spent_by_category)
        self.assertEqual(response.data["balance"], str(total_income - total_expense))

    def test_get_summary_invalid_month(self):
        month_ahead = f"{self.date.month + 1:02d}"
        url = reverse(
            "summary-get-summary",
            kwargs={"year": self.year, "month": month_ahead},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_summary_invalid_year(self):
        url = reverse(
            "summary-get-summary", kwargs={"year": self.year + 1, "month": self.month}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
