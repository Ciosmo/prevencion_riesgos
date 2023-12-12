from django import forms
from .models import AccidenteLaboral, EconomicActivity, Region, Category


class AccidenteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar el queryset para incluir solo actividades con ID del 1 al 17
        queryset_actividad = EconomicActivity.objects.filter(id__in=range(1, 18))
        queryset_region = Region.objects.filter(id__in=range(1, 17))
        queryset_tipo_accidente = Category.objects.filter(id__in=[1, 2, 6])

        # Agregar '----------' al principio del queryset para actividad_economica
        choices_actividad = [(None, '----------')] + [(obj.id, str(obj)) for obj in queryset_actividad]
        self.fields['actividad_economica'].choices = choices_actividad
        self.fields['actividad_economica'].required = True

        # Agregar '----------' al principio del queryset para region
        choices_region = [(None, '----------')] + [(obj.id, str(obj)) for obj in queryset_region]
        self.fields['region'].choices = choices_region
        self.fields['region'].required = True

        # Agregar '----------' al principio del queryset para tipo_accidente
        choices_tipo_accidente = [(None, '----------')] + [(obj.id, str(obj)) for obj in queryset_tipo_accidente]
        self.fields['tipo_accidente'].choices = choices_tipo_accidente
        self.fields['tipo_accidente'].required = True

    class Meta:
        model = AccidenteLaboral
        fields = '__all__'
        widgets = {
            'fecha_accidente': forms.TextInput(attrs={'type': 'date'}),
            'hora_accidente': forms.TextInput(attrs={'type': 'time'}),
        }

