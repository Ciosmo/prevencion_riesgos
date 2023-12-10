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

    actividad_economica = forms.ModelChoiceField(queryset=EconomicActivity.objects.all())
    comuna = forms.ChoiceField(choices=COMUNAS_CHOICES, label='Comuna')

    class Meta:
        model = AccidenteLaboral
        fields = '__all__'
        widgets = {
            'fecha_accidente': forms.TextInput(attrs={'type': 'date'}),
            'hora_accidente': forms.TextInput(attrs={'type': 'time'}),
        }

