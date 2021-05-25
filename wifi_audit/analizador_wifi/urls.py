from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_dispositivos, name="Dispositivos"),
    path('wifi', views.analizador_wifi, name="Wifi"),
    path('<int:id>/informacion_dispositivo', views.dispositivo_info, name="DispositivoInfo"),
]
