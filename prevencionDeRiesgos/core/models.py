from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)

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

class AccidenteLaboral(models.Model):
    nombre_empleado = models.CharField(max_length=255)
    actividad_economica = models.CharField(max_length=255)
    genero = models.CharField(max_length=10, choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')])
    comuna = models.CharField(max_length=255)
    fecha_accidente = models.DateField()
    hora_accidente = models.TimeField()
    tipo_accidente = models.CharField(max_length=50, choices=[('trabajo', 'Trabajo'), ('trayecto', 'Trayecto')])
    descripcion_accidente = models.TextField()

    def __str__(self):
        return f"{self.nombre_empleado} - {self.fecha_accidente}"