from django import forms
from .models import AccidenteLaboral, EconomicActivity

COMUNAS_CHOICES = [
    ('--------', '---------'),
    ('ancud', 'Ancud'),
    ('angol', 'Angol'),
    ('antofagasta', 'Antofagasta'),
    ('arica', 'Arica'),
    ('cauquenes', 'Cauquenes'),
    ('calama', 'Calama'),
    ('caldera', 'Caldera'),
    ('castro', 'Castro'),
    ('chanaral', 'Chañaral'),
    ('chillan', 'Chillán'),
    ('concepcion', 'Concepción'),
    ('constitucion', 'Constitución'),
    ('coquimbo', 'Coquimbo'),
    ('coronel', 'Coronel'),
    ('curico', 'Curicó'),
    ('futrono', 'Futrono'),
    ('huasco', 'Huasco'),
    ('illapel', 'Illapel'),
    ('la florida', 'La Florida'),
    ('la serena', 'La Serena'),
    ('la union', 'La Unión'),
    ('las condes', 'Las Condes'),
    ('linares', 'Linares'),
    ('los angeles', 'Los Ángeles'),
    ('machali', 'Machalí'),
    ('maipu', 'Maipú'),
    ('mejillones', 'Mejillones'),
    ('melipilla', 'Melipilla'),
    ('osorno', 'Osorno'),
    ('ovalle', 'Ovalle'),
    ('padre_las_casas', 'Padre Las Casas'),
    ('panguipulli', 'Panguipulli'),
    ('punta arenas', 'Punta Arenas'),
    ('puerto montt', 'Puerto Montt'),
    ('puerto natales', 'Puerto Natales'),
    ('puerto varas', 'Puerto Varas'),
    ('puerto williams', 'Puerto Williams'),
    ('putre', 'Putre'),
    ('quillota', 'Quillota'),
    ('quilpue', 'Quilpué'),
    ('rancagua', 'Rancagua'),
    ('rengo', 'Rengo'),
    ('rio bueno', 'Río Bueno'),
    ('san antonio', 'San Antonio'),
    ('san fernando', 'San Fernando'),
    ('santiago', 'Santiago'),
    ('sierra gorda', 'Sierra Gorda'),
    ('talca', 'Talca'),
    ('talcahuano', 'Talcahuano'),
    ('temuco', 'Temuco'),
    ('tocopilla', 'Tocopilla'),
    ('valdivia', 'Valdivia'),
    ('valparaiso', 'Valparaíso'),
    ('vallenar', 'Vallenar'),
    ('valparaiso', 'Valparaíso'),
    ('victoria', 'Victoria'),
    ('villa alemana', 'Villa Alemana'),
    ('villarrica', 'Villarrica'),
    ('vinadelmar', 'Viña del Mar'),
    ('vicuna', 'Vicuña'),
]

class AccidenteForm(forms.ModelForm):
    comuna = forms.ChoiceField(choices=COMUNAS_CHOICES, label='Comuna')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar el queryset para incluir solo actividades con ID del 1 al 17
        queryset = EconomicActivity.objects.filter(id__in=range(1, 18))

        # Agregar '----------' al principio del queryset
        choices = [('', '----------')] + [(obj.id, str(obj)) for obj in queryset]
        self.fields['actividad_economica'].choices = choices
        self.fields['actividad_economica'].required = True  # Hacer el campo requerido

        # Agregar script JS al widget del campo para establecer el valor predeterminado
        self.fields['actividad_economica'].widget.attrs['onload'] = "this.value='';"

    class Meta:
        model = AccidenteLaboral
        fields = '__all__'
        widgets = {
            'fecha_accidente': forms.TextInput(attrs={'type': 'date'}),
            'hora_accidente': forms.TextInput(attrs={'type': 'time'}),
        }

