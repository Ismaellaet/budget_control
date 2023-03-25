from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class BaseBudgetViewSet(viewsets.ModelViewSet):
    """ 
    Base viewset for Expense and Income viewsets
    """
    serializer_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["description"]

    @action(detail=False, url_path="(?P<year>[0-9]{4})/(?P<month>[0-9]{2})", url_name="by-year-month")
    def get_by_year_month(self, request: Request, year: str, month: str) -> Response:
        """
        Return a list of objects filtered by year and month
        """
        queryset = self.queryset.filter(date__year=year, date__month=month)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
