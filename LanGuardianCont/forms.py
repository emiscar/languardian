from django import forms
from django.forms import formset_factory


class DispositivoForm(forms.Form):
    opciones = [('1', 'SSH'), ('2', 'Telnet')]
    ip = forms.GenericIPAddressField(label="Dirección IP", required=True, widget=forms.TextInput(
        attrs={
            'style': 'width: 120px; font-size: smaller; color: black; border-radius: 10px; height: 30px;',
        }),
        error_messages={
        'required': "Requerido",
        'invalid':"Formato incorrecto"
    })
    usuario = forms.CharField(label="Usuario", required=True, widget=forms.TextInput(
        attrs={
            'style': 'width: 120px; font-size: smaller;color: black; border-radius: 10px; height: 30px;',
            'min': "3",
        }),
        error_messages={
        'required': "Requerido"
    })
    clave = forms.CharField(label="Clave", required=True, widget=forms.PasswordInput(
        attrs={
            'style': 'width: 120px; font-size: smaller;color: black; border-radius: 10px; height: 30px;',
            'min': "1",
        }),
        error_messages={
        'required': "Requerido"
    })
    protocolo = forms.ChoiceField(label="Protocolo", required=True, choices=opciones, widget=forms.Select(
        attrs={
            'style': 'width: 100px; font-size: smaller; color: black; border-radius: 10px; height: 30px;',
        }),
        error_messages={
        'required': "Requerido"
    })
    puerto = forms.CharField(label="Puerto", required=True, widget=forms.NumberInput(
        attrs={
            'style': 'width: 80px; font-size: smaller;color: black; border-radius: 10px; height: 30px;',
            'min': "1",
            'max': "65536",
        }),
        error_messages={
        'required': "Requerido"
    })

DispositivoFormSet = formset_factory(
    DispositivoForm, extra=1, max_num=5
)