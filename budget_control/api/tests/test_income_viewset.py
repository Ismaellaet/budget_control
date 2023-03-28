from datetime import datetime

from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase
from rest_framework import status

from ...models import Income
from ..serializers.incomes import IncomeSerializer


class IncomeViewSetTestCase(APITestCase):
    def setUp(self):
        self.incomes = baker.make("Income", 2)

    def test_list_incomes(self):
        response = self.client.get(reverse("income-list"))
        serializer = IncomeSerializer(self.incomes, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_income(self):
        valid_data = {
            "description": "Income 3",
            "value": "503.00",
            "date": "2022-02-28",
        }
        response = self.client.post(path=reverse("income-list"), data=valid_data)
        income = Income.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(income.description, valid_data["description"])
        self.assertEqual(str(income.value), valid_data["value"])
        self.assertEqual(str(income.date), valid_data["date"])

    def test_create_invalid_income(self):
        invalid_payload = {
            "description": "",
            "value": "1000.00",
            "date": "2022-02-15",
        }
        response = self.client.post(path=reverse("income-list"), data=invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_income(self):
        income = self.incomes[0]
        response = self.client.get(reverse("income-detail", args=[income.id]))
        income = Income.objects.get(id=income.id)
        serializer = IncomeSerializer(income)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_income(self):
        income = self.incomes[0]
        data = {
            "description": "Updated Income",
            "value": "6000.00",
            "date": "2022-03-01",
        }

        url = reverse("income-detail", args=[income.id])
        response = self.client.put(path=url, data=data)
        income.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(income.description, data["description"])
        self.assertEqual(str(income.value), data["value"])
        self.assertEqual(str(income.date), data["date"])

    def test_delete_income(self):
        income = self.incomes[0]
        url = reverse("income-detail", args=[income.id])
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Income.objects.filter(id=income.id).exists())


class IncomeByYearMonthTestCase(APITestCase):
    def setUp(self):
        self.date = datetime.now()
        self.year = self.date.year
        self.month = f"{self.date:%m}"
        self.incomes = baker.make("Income", 2, date=self.date)

    def test_must_get_incomes_by_year_month(self):
        url = reverse("income-by-year-month", args=[self.year, self.month])
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for income in response.data:
            income_date = datetime.strptime(income["date"], "%Y-%m-%d")
            self.assertEqual(income_date.year, self.year)
            self.assertEqual(f"{income_date.month:02d}", self.month)
