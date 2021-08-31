from django.db import models

# Create your models here.

class Dispositivo(models.Model):
    ip = models.CharField(max_length=15, blank=False, null=False, unique=True)
    puerto = models.IntegerField(blank=False, null=False)
    usuario = models.CharField(max_length=50, blank=False, null=False)
    clave = models.CharField(max_length=50, blank=False, null=False)
    protocolo = models.CharField(max_length=50)
    
    def __str__(self):
    	return self.ip