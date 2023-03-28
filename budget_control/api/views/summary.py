from django.db.models import Sum, QuerySet

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from ...models import Expense, Income
from ..serializers.summary import SummarySerializer


class SummaryViewSet(viewsets.ViewSet):
    @action(detail=False, url_path="(?P<year>[0-9]{4})/(?P<month>[0-9]{2})")
    def get_summary(self, request: Request, year: str, month: str) -> Response:
        try:
            incomes = Income.objects.filter(date__year=year, date__month=month)
            expenses = Expense.objects.filter(date__year=year, date__month=month)

            summary_data = {
                "total_income": self.get_total(incomes),
                "total_expense": self.get_total(expenses),
                "balance": self.get_balance(incomes, expenses),
                "total_spent_by_category": self.get_total_spent_by_category(expenses),
            }

            serializer = SummarySerializer(summary_data)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid year or month"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_balance(self, incomes: QuerySet[Income], expenses: QuerySet[Expense]):
        return self.get_total(incomes) - self.get_total(expenses)

    @staticmethod
    def get_total(queryset: QuerySet):
        return queryset.aggregate(total=Sum("value") or 0)["total"]

    @staticmethod
    def get_total_spent_by_category(expenses: QuerySet[Expense]):
        categories_expenses = expenses.values("category").annotate(total=Sum("value"))
        return {
            expense["category"]: expense["total"] for expense in categories_expenses
        }
