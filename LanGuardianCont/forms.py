from django import forms
from django.forms import modelformset_factory
from .models import Dispositivo

class DispositivoForm(forms.ModelForm):
    opciones=[('1', 'Telnet'),('2', 'SSH')]
    ip=forms.CharField(label="Dirección IP", required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Ingrese IP del dispositivo',
            'style':'width: 200px; font-size: smaller;',
        }
    ))
    puerto=forms.CharField(label="Puerto", required=True, widget=forms.NumberInput(
        attrs={
            'placeholder':'Ingrese puerto SSH/Telnet',
            'style':'width: 200px; font-size: smaller;',
        }
    ))
    usuario=forms.CharField(label="Usuario", required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Ingrese usuario',
            'style':'width: 200px; font-size: smaller;',
        }
    ))
    clave = forms.CharField(label="Clave", required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder':'Ingrese contraseña',
            'style':'width: 200px; font-size: smaller;'            
        }
    ))
    protocolo = forms.ChoiceField(label="Protocolo", required=True, widget=forms.Select, choices=opciones)

    class Meta:
        model = Dispositivo
        fields = (
            'ip',
            'puerto',
            'usuario',
            'clave',
            'protocolo',
        )

DispositivoFormSet = modelformset_factory(
    Dispositivo, DispositivoForm, extra=1
)