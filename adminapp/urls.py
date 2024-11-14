# adminapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #Authentication Routes
    path('', views.login_view, name='login'),
    path('dashboard', views.dashboard_home, name='dashboard_home'),

    #Results Managment Routes
    path('results/upload', views.dashboard_upload_results, name='results_upload'),
    path('results', views.dashboard_home, name='results_view'),
    path('results/analysis', views.dashboard_home, name='results_analysis'),
    path('results/spreadsheet/generate', views.dashboard_home, name='results_spreadsheet_generate'),

    #Student Management Routes
    path('students/manage', views.dashboard_home, name='students_manage'),
    path('students/registration', views.dashboard_home, name='student_registration'),
    path('students', views.dashboard_home, name='students'),

    #Settings Routes
    path('settings/system', views.dashboard_home, name='settings_system'),
    path('settings/profile', views.dashboard_home, name='settings_profile'),

]
