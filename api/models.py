from django.db import models


class Income(models.Model):
    description = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.date} => {self.description}: R${self.value}"


class Expense(models.Model):
    description = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.date} => {self.description}: -R${self.value}"
