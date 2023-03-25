from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from api.models import Income
from api.serializers import IncomeSerializer


class IncomeViewSetTestCase(APITestCase):
    def setUp(self):
        self.income1 = Income.objects.create(
            description="Income 1", value="5000.00", date=datetime.now().date()
        )
        self.income2 = Income.objects.create(
            description="Income 2", value="1000.00", date=datetime.now().date()
        )

    def test_list_incomes(self):
        response = self.client.get(reverse("income-list"))
        incomes = Income.objects.all()
        serializer = IncomeSerializer(incomes, many=True)

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
        response = self.client.get(reverse("income-detail", args=[self.income1.id]))
        income = Income.objects.get(id=self.income1.id)
        serializer = IncomeSerializer(income)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_income(self):
        data = {
            "description": "Updated Income",
            "value": "6000.00",
            "date": "2022-03-01",
        }
        url = reverse("income-detail", args=[self.income1.id])
        response = self.client.put(path=url, data=data)
        self.income1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.income1.description, data["description"])
        self.assertEqual(str(self.income1.value), data["value"])
        self.assertEqual(str(self.income1.date), data["date"])

    def test_delete_income(self):
        url = reverse("income-detail", args=[self.income1.id])
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Income.objects.filter(id=self.income1.id).exists())


class IncomeByYearMonthTestCase(APITestCase):
    def setUp(self):
        self.date = datetime.now()
        self.income1 = Income.objects.create(
            description="Income 1", value="200.30", date=self.date.date()
        )
        self.income2 = Income.objects.create(
            description="Income 2", value="90.10", date=self.date.date()
        )
        self.year = self.date.year
        self.month = f"{self.date:%m}"

    def test_must_get_incomes_by_year_month(self):
        url = reverse("income-by-year-month", args=[self.year, self.month])
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for income in response.data:
            income_date = datetime.strptime(income["date"], "%Y-%m-%d")
            self.assertEqual(income_date.year, self.year)
            self.assertEqual(f"{income_date.month:02d}", self.month)
