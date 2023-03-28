from rest_framework import routers

from .views.expenses import ExpenseViewSet
from .views.incomes import IncomeViewSet
from .views.summary import SummaryViewSet

router_api = routers.DefaultRouter()
router_api.register(r"incomes", IncomeViewSet)
router_api.register(r"expenses", ExpenseViewSet)
router_api.register(r"summary", SummaryViewSet, basename="summary")
