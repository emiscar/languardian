from django.urls import path
from LanGuardianApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="Inicio"),
    path('categorias/',views.categorias, name="Categorias"),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
