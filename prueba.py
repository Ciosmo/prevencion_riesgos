from django.db import models

class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return f"{self.year}"

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class EconomicActivity(models.Model):
    activity_name = models.CharField(max_length=255)

    def __str__(self):
        return self.activity_name

class Mutualidad(models.Model):
    mutualidad_name = models.CharField(max_length=255)

    def __str__(self):
        return self.mutualidad_name
    
class Region(models.Model):
    region = models.CharField(max_length=255)

    def __str__(self):
        return self.region

class DiasxActividad(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class DiasxMut(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    mutual = models.ForeignKey(Mutualidad, on_delete=models.CASCADE, default=1)
    anio2018 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2019 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2020 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2021 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    anio2022 = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class TasaxAct(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class AccidentesxSexo(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    men = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    women = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class PorcentajexAct(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class FallecidosxAct(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    isl = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class FallecidosxSexo(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    EconomicActivity = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    men = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    women = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class AccidentesxRegion(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE,default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    achs = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    museg = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class AccidenteLaboral(models.Model):
    nombre_empleado = models.CharField(max_length=255)
    actividad_economica = models.ForeignKey(EconomicActivity, on_delete=models.CASCADE, default=1)
    genero = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], null=True)
    comuna = models.CharField(max_length=255)
    fecha_accidente = models.DateField()
    hora_accidente = models.TimeField()
    tipo_accidente = models.CharField(max_length=50, choices=[('Trabajo', 'Trabajo'), ('Trayecto', 'Trayecto')])
    descripcion_accidente = models.TextField()

    def __str__(self):
        return f"{self.nombre_empleado} - {self.fecha_accidente}"