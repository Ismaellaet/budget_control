from rest_framework import serializers


class SummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=6, decimal_places=2)
    balance = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_spent_by_category = serializers.DictField(child=serializers.DecimalField(max_digits=6, decimal_places=2))
