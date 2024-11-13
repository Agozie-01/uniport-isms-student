# adminapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard', views.dashboard_view, name='dashboard_home'),
    #path('results/upload', views.dashboard_view, name='dashboard_home'),
]
