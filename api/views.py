from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from .models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description"]

    @action(detail=False, url_path="(?P<year>[0-9]{4})/(?P<month>[0-9]{2})", url_name="by-year-month")
    def incomes_by_year_month(self, request: Request, year: str, month: str) -> Response:
        incomes = self.queryset.filter(date__year=year, date__month=month)
        serializer = self.serializer_class(incomes, many=True)
        return Response(serializer.data)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description"]

    @action(detail=False, url_path="(?P<year>[0-9]{4})/(?P<month>[0-9]{2})", url_name="by-year-month")
    def expenses_by_year_month(self, request: Request, year: str, month: str) -> Response:
        expenses = self.queryset.filter(date__year=year, date__month=month)
        serializer = self.serializer_class(expenses, many=True)
        return Response(serializer.data)
