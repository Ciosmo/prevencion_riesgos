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
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Mutualidad(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    mutual = models.CharField(max_length=255)
    anio2018 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2019 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2020 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2021 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2022 = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Tasa_Eco_Act(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Sexo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    men = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    women = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)