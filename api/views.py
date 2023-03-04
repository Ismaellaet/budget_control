from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description"]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description"]
