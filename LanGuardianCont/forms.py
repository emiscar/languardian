#from LanGuardianCont.models import Dispositivo
from django import forms
#from django.forms import fields, models

class formularioCont(forms.Form):
    ip=forms.CharField(label="Dirección IP", required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'inputIP',
            'placeholder':'Ingrese IP del dispositivo',
            'style':'width: 200px; font-size: smaller;',
        }
    ))
    puerto=forms.CharField(label="Puerto", required=True, widget=forms.NumberInput(
        attrs={
            'class':'form-control',
            'id':'inputPuerto',
            'placeholder':'Ingrese puerto SSH/Telnet',
            'style':'width: 200px; font-size: smaller;',
        }
    ))
    usuario=forms.CharField(label="Usuario", required=True, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'id':'inputUsuario',
            'placeholder':'Ingrese usuario',
            'style':'width: 200px; font-size: smaller;',
        }
    ))
    clave=forms.CharField(label="Clave", required=True, widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'id':'inputClave',
            'placeholder':'Ingrese contraseña',
            'style':'width: 200px; font-size: smaller;'            
        }
    ))

#class DispositivoForm(forms.ModelForm):

#    class Meta:
#        model = Dispositivo
#        fields = (
#            'ip',
#            'puerto',
#            'usuario',
#            'clave',
#        )