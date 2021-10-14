from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):

    return render(request,"LanGuardianApp/home.html")

def categorias(request):

    return render(request,"LanGuardianApp/categorias.html")