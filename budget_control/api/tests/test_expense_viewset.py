from datetime import datetime

from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase
from rest_framework import status

from ...models import Expense
from ..serializers.expenses import ExpenseSerializer


class ExpenseBasicCrudTestCase(APITestCase):
    def setUp(self):
        self.expenses = baker.make("Expense", 2)

    def test_list_expenses(self):
        response = self.client.get(reverse("expense-list"))
        serializer = ExpenseSerializer(self.expenses, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_expense(self):
        valid_data = {
            "description": "Expense 3",
            "value": "100.50",
            "date": "2022-02-28",
        }
        response = self.client.post(path=reverse("expense-list"), data=valid_data)
        expense = Expense.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expense.description, valid_data["description"])
        self.assertEqual(str(expense.value), valid_data["value"])
        self.assertEqual(str(expense.date), valid_data["date"])

    def test_create_invalid_expense(self):
        invalid_data = {
            "description": "",
            "value": "100.50",
            "date": "2022-02-28",
        }
        response = self.client.post(path=reverse("expense-list"), data=invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_expense(self):
        expense = self.expenses[0]
        response = self.client.get(
            reverse("expense-detail", args=[expense.id])
        )
        expense = Expense.objects.get(id=expense.id)
        serializer = ExpenseSerializer(expense)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_expense(self):
        expense = self.expenses[0]
        data = {
            "description": "Updated Expense",
            "value": "99.99",
            "date": "2022-02-27",
        }

        url = reverse("expense-detail", args=[expense.id])
        response = self.client.put(path=url, data=data)
        expense.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expense.description, data["description"])
        self.assertEqual(str(expense.value), data["value"])
        self.assertEqual(str(expense.date), data["date"])

    def test_delete_expense(self):
        expense = self.expenses[0]
        url = reverse("expense-detail", args=[expense.id])
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=expense.id).exists())


class ExpenseByYearMonthTestCase(APITestCase):
    def setUp(self):
        self.date = datetime.now()
        self.year = self.date.year
        self.month = f"{self.date:%m}"
        self.expenses = baker.make("Expense", 2, date=self.date)

    def test_must_get_expenses_by_year_month(self):
        url = reverse("expense-by-year-month", args=[self.year, self.month])
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for expense in response.data:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            self.assertEqual(expense_date.year, self.year)
            self.assertEqual(f"{expense_date.month:02d}", self.month)
