from django.urls import path
from . import views
from .views import DispositivosView

urlpatterns = [
    path('', DispositivosView.as_view(), name="Analisis"),
    path('configuracion/',views.configuracion, name="Config"),
]