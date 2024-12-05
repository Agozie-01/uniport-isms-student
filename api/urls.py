from django.urls import re_path

from .views import (
    StudentView, 
    AdminView, 
    DepartmentView, 
    CurrentUserView, 
    DashboardStatsView, 
    RecentActivitiesView,
    CoursePerformanceTrendView,
    CourseView,
    SemesterView,
    SessionView,
    UploadResultsView,
    FetchResultsView,
    GenerateSpreadsheetView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    # Authentication endpoints
    re_path(r'^token/?$', TokenObtainPairView.as_view(), name='auth_token'),  # Optional trailing slash
    re_path(r'^token/refresh/?$', TokenRefreshView.as_view(), name='auth_token_refresh'),  # Optional trailing slash
    re_path(r'^token/logout/?$', TokenBlacklistView.as_view(), name='auth_token_logout'),

    # Student endpoints
    re_path(r'^students/?$', StudentView.as_view(), name='students'),  # Optional trailing slash
    re_path(r'^students/(?P<student_id>\d+)/?$', StudentView.as_view(), name='student_detail'),  # Optional trailing slash

    # Admin endpoints
    re_path(r'^admins/?$', AdminView.as_view(), name='admin_new'),  # Optional trailing slash
    re_path(r'^admins/(?P<admin_id>\d+)/?$', AdminView.as_view(), name='admin_detail'),
    re_path(r'^user/me/?$', CurrentUserView.as_view(), name='current_user'),

    # Departments
    re_path(r'^departments/?$', DepartmentView.as_view(), name='departments'),  # List/Create
    re_path(r'^departments/(?P<department_id>\d+)/?$', DepartmentView.as_view(), name='department_detail'),  # Retrieve/Update/Delete

    # Dashboard
    re_path(r'^dashboard/stats/?$', DashboardStatsView.as_view(), name='dashboard'),

    # Activity log
    re_path(r'^activities/recent/?$', RecentActivitiesView.as_view(), name='recent_activities'),

    # Courses
    re_path(r'^courses/performance-trend/?$', CoursePerformanceTrendView.as_view(), name='course_performance_trend'),
    re_path(r'^courses/?$', CourseView.as_view(), name='course_list_create'),  # For listing and creating courses
    re_path(r'^courses/(?P<course_id>\d+)/?$', CourseView.as_view(), name='course_detail'),  # For getting, updating, and deleting specific courses

    # Semesters
    re_path(r'^semesters/?$', SemesterView.as_view(), name='semester_list_create'),  # List all semesters and create new one
    re_path(r'^semesters/(?P<semester_id>\d+)/?$', SemesterView.as_view(), name='semester_detail'),  # Get, update, and delete a specific semester

    # Sessions
    re_path(r'^sessions/?$', SessionView.as_view(), name='session_list_create'),  # List all sessions and create new one
    re_path(r'^sessions/(?P<session_id>\d+)/?$', SessionView.as_view(), name='session_detail'),  # Get, update, and delete specific sessions

    # Result Management
    re_path(r"^results/?$", FetchResultsView.as_view(), name="fetch_results"),
    re_path(r"^^results/spreadsheet/(?P<student_id>\d+)/?$", GenerateSpreadsheetView.as_view(), name="generate_spreadsheet"),
    re_path(r"^results/upload/?$", UploadResultsView.as_view(), name="upload_results"),
]
