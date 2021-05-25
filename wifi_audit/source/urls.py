from django.urls import path

import modo_monitor.views
from source import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/aps', permanent=False), name='Home'),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
]