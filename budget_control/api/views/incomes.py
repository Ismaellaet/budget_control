from ...models import Income
from ..serializers.incomes import IncomeSerializer
from .base import BaseBudgetViewSet


class IncomeViewSet(BaseBudgetViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
