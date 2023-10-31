from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

class EconomicActivity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    