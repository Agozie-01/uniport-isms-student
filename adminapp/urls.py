# adminapp/urls.py
from django.urls import re_path
from . import views

urlpatterns = [
    # Authentication Routes
    re_path(r'^$', views.login_view, name='login'),  # Root URL
    re_path(r'^dashboard/?$', views.dashboard_home, name='dashboard_home'),

    # Results Management Routes
    re_path(r'^results/upload/?$', views.dashboard_upload_results, name='results_upload'),
    re_path(r'^results/?$', views.dashboard_home, name='results_view'),
    re_path(r'^results/analysis/?$', views.dashboard_home, name='results_analysis'),
    re_path(r'^results/spreadsheet/generate/?$', views.dashboard_home, name='results_spreadsheet_generate'),

    # Student Management Routes
    re_path(r'^students/manage/?$', views.dashboard_home, name='students_manage'),
    re_path(r'^students/registration/?$', views.dashboard_home, name='student_registration'),
    re_path(r'^students/?$', views.dashboard_home, name='students'),

    # Settings Routes
    re_path(r'^settings/system/?$', views.dashboard_home, name='settings_system'),
    re_path(r'^settings/profile/?$', views.dashboard_home, name='settings_profile'),
]
