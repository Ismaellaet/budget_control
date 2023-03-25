from ...models import Expense
from ..serializers.expenses import ExpenseSerializer
from .base import BaseBudgetViewSet


class ExpenseViewSet(BaseBudgetViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
