from rest_framework import routers

from .views.expenses import ExpenseViewSet
from .views.incomes import IncomeViewSet


router_api = routers.DefaultRouter()
router_api.register(r"incomes", IncomeViewSet)
router_api.register(r"expenses", ExpenseViewSet)
