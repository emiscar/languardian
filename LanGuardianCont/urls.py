from django.urls import path
from . import views

urlpatterns = [
    path('',views.analisis, name="Analisis"),
    path('configuracion/',views.configuracion, name="Config"),
]