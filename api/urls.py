from django.urls import re_path
from .views import StudentView, AdminView, DepartmentView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Authentication endpoints
    re_path(r'^token/?$', TokenObtainPairView.as_view(), name='auth_token'),  # Optional trailing slash
    re_path(r'^token/refresh/?$', TokenRefreshView.as_view(), name='auth_token_refresh'),  # Optional trailing slash

    # Student endpoints
    re_path(r'^students/?$', StudentView.as_view(), name='students'),  # Optional trailing slash
    re_path(r'^students/(?P<student_id>\d+)/?$', StudentView.as_view(), name='student_detail'),  # Optional trailing slash

    # Admin endpoints
    re_path(r'^admins/?$', AdminView.as_view(), name='admin_new'),  # Optional trailing slash
    re_path(r'^admins/(?P<admin_id>\d+)/?$', AdminView.as_view(), name='admin_detail'),

    re_path(r'^departments/?$', DepartmentView.as_view(), name='departments'),  # List/Create
    re_path(r'^departments/(?P<department_id>\d+)/?$', DepartmentView.as_view(), name='department_detail'),  # Retrieve/Update/Delete

]
