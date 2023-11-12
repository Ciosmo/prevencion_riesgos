from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=255)

class Year(models.Model):
    year =models.IntegerField

class EconomicActivity(models.Model):
    activity_name = models.CharField(max_length=255)

class Mutulidad(models.Model):
    name = models.CharField(max_length=255)

class Sexo(models.Model):
    sexo = models.CharField(max_length=255)

class FactAccidente(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    Year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    Mutulidad = models.ForeignKey(Mutulidad, on_delete=models.CASCADE, default=1)
    Sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, default=1)
    Mutulidad = models.ForeignKey(Mutulidad, on_delete=models.CASCADE, default=1)