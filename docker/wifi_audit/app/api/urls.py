from django.urls import path
from . import views

urlpatterns = [
    path('aps', views.APIApView.as_view(), name = "api-aps"),
    path('devices', views.APDeviceView.as_view(), name="api-devices"),
    path('clients', views.APClientsView.as_view(), name="api-clients"),
]


