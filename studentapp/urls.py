from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_login, name='student_login'),
    path('dashboard/', views.dashboard, name='student_dashboard'),
]
