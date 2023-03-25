from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from api.models import Expense
from api.serializers import ExpenseSerializer


class ExpenseBasicCrudTestCase(APITestCase):
    def setUp(self):
        self.expense1 = Expense.objects.create(
            description="Expense 1", value="50.99", date=datetime.now().date()
        )
        self.expense2 = Expense.objects.create(
            description="Expense 2", value="75.30", date=datetime.now().date()
        )

    def test_list_expenses(self):
        response = self.client.get(reverse("expense-list"))
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)

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
        response = self.client.get(reverse("expense-detail", args=[self.expense1.id]))
        expense = Expense.objects.get(id=self.expense1.id)
        serializer = ExpenseSerializer(expense)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_expense(self):
        data = {
            "description": "Updated Expense",
            "value": "99.99",
            "date": "2022-02-27",
        }
        url = reverse("expense-detail", args=[self.expense1.id])
        response = self.client.put(path=url, data=data)
        self.expense1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.expense1.description, data["description"])
        self.assertEqual(str(self.expense1.value), data["value"])
        self.assertEqual(str(self.expense1.date), data["date"])

    def test_delete_expense(self):
        url = reverse("expense-detail", args=[self.expense2.id])
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense2.id).exists())


class ExpenseByYearMonthTestCase(APITestCase):
    def setUp(self):
        self.date = datetime.now()
        self.expense1 = Expense.objects.create(
            description="Expense 1", value="50.99", date=self.date.date()
        )
        self.expense2 = Expense.objects.create(
            description="Expense 2", value="75.30", date=self.date.date()
        )
        self.year = self.date.year
        self.month = f"{self.date:%m}"

    def test_must_get_expenses_by_year_month(self):
        url = reverse("expense-by-year-month", args=[self.year, self.month])
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for expense in response.data:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            self.assertEqual(expense_date.year, self.year)
            self.assertEqual(f"{expense_date.month:02d}", self.month)
