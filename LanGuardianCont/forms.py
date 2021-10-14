from django import forms
from django.forms import modelformset_factory
from .models import Dispositivo

class DispositivoForm(forms.ModelForm):
    opciones=[('1', 'Telnet'),('2', 'SSH')]
    ip=forms.CharField(label="Dirección IP", required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Ingrese IP del dispositivo',
            'style':'width: 200px; font-size: smaller; color: black;',
            #'class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-radius-10 u-white',
        }
    ))
    usuario=forms.CharField(label="Usuario", required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Ingrese usuario',
            'style':'width: 200px; font-size: smaller;color: black;',
            #'class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-radius-10 u-white',
        }
    ))
    clave = forms.CharField(label="Clave", required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder':'Ingrese contraseña',
            'style':'width: 200px; font-size: smaller;color: black;',
            #'class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-radius-10 u-white',
        }
    ))
    protocolo = forms.ChoiceField(label="Protocolo", required=True, widget=forms.Select(attrs={'style':'color: black;'}), choices=opciones)#(
        #attrs={'class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-radius-10 u-white'})
    puerto=forms.CharField(label="Puerto", required=True, widget=forms.NumberInput(
        attrs={
            'placeholder':'Ingrese puerto SSH/Telnet',
            'style':'width: 200px; font-size: smaller;color: black;',
            #'class':'u-border-1 u-border-grey-30 u-input u-input-rectangle u-radius-10 u-white',
        }
    ))
    
    

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
    Dispositivo, DispositivoForm, extra=1, max_num=5
)