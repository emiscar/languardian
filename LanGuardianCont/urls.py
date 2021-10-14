from django.urls import path
from . import views
from .views import DispositivosView

urlpatterns = [
    path('', DispositivosView.as_view(), name="Analisis"),
    path('configuracion/',views.configuracion, name="Config"),
    #path('reporte',views.reporte, name="Reporte"),
    path('reporte2',views.report_pdf, name="Reporte2"),
]