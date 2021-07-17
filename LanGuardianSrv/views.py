from django.shortcuts import render
from LanGuardianSrv.models import Servicio

# Create your views here.

def servicios(request):

    servicios=Servicio.objects.all()
    return render(request,"LanGuardianSrv/servicios.html", {"servicios": servicios})