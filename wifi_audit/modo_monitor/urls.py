from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_aps, name="APs"),
    path('monitor', views.modo_monitor, name="Monitor"),
    path('paquetes', views.captura_paquetes, name="Paquetes"),
    path('<int:id>/informacion', views.ap_info, name="ApInfo"),
    path('<int:id>/senal', views.ap_senal, name="ApSenal"),
    path('<int:id>/seguridad', views.ap_seguridad, name="ApSeguridad"),
    path('<int:id>/connection', views.connection, name="Connection"),
    path('<int:id>/connected', views.connected, name="Connected"),
    path('<int:id>/personal_scan', views.personal_scan, name="PersonalScan"),
]
