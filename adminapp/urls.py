# adminapp/urls.py
from django.urls import re_path
from . import views

urlpatterns = [
    # Authentication Routes
    re_path(r'^$', views.login_view, name='login'),  # Root URL
    re_path(r'^dashboard/?$', views.home, name='home'),

    # Results Management Routes
    re_path(r'^results/?$', views.results, name='results_view'),

    # Management Routes
    re_path(r'^students/?$', views.students, name='students_page'),
    re_path(r'^departments/?$', views.departments, name='departments_page'),
    re_path(r'^semesters/?$', views.semesters, name='semesters_page'),
    re_path(r'^sessions/?$', views.sessions, name='sessions_page'),

    # Settings Routes
    re_path(r'^settings/system/?$', views.home, name='settings_system'),
    re_path(r'^settings/profile/?$', views.home, name='settings_profile'),
]
