from rest_framework import routers

from .views import IncomeViewSet, ExpenseViewSet


router_api = routers.DefaultRouter()
router_api.register(r"incomes", IncomeViewSet)
router_api.register(r"expenses", ExpenseViewSet)
