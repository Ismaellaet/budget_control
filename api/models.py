from django.db import models


class Income(models.Model):
    description = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.date} => {self.description}: R${self.value}"


class Expense(models.Model):
    CATEGORIES = [
        ("food", "food"),
        ("health", "health"),
        ("housing", "housing"),
        ("transportation", "transportation"),
        ("education", "education"),
        ("leisure", "leisure"),
        ("unforeseen", "unforeseen"),
        ("other", "other"),
    ]
    description = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORIES, default="other")

    def __str__(self) -> str:
        return f"{self.date} => {self.description}: -R${self.value}"
