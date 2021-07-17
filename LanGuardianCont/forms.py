from django import forms

class formularioCont(forms.Form):
    ip=forms.CharField(label="Dirección IP", required=True)
    puerto=forms.CharField(label="Puerto", required=True)
    usuario=forms.CharField(label="Usuario", required=True)
    clave=forms.CharField(label="Clave", required=True)
    