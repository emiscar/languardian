from django.urls import path
from . import views

urlpatterns = [
    #path('',views.AgDispo.as_view(), name="Analisis"),
    path('',views.analisis, name="Analisis"),
    path('configuracion/',views.configuracion, name="Config"),
]