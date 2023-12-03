from django import forms
from .models import AccidenteLaboral

class AccidenteForm(forms.ModelForm):
    class Meta:
        model = AccidenteLaboral
        fields = '__all__'
        widgets = {
            'fecha_accidente': forms.TextInput(attrs={'type': 'date'}),
            'hora_accidente': forms.TextInput(attrs={'type': 'time'}),
        }

