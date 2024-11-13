from django.shortcuts import render
from django.urls import reverse
from adminapp.models import Test

def dashboard_view(request):
    # Define the sidebar menu with groups and items
    sidebar_menu = [
        {
            "name": "Dashboard",
            "items": [
                {"name": "Overview", "link": reverse('dashboard_home'), "icon": "grid"},
            ]
        },
        {
            "name": "Result Management",
            "items": [
                {"name": "Upload Results", "link": "#", "icon": "upload"},
                {"name": "View Results", "link": "#", "icon": "eye"},
                {"name": "Result Analysis", "link": "#", "icon": "bar-chart-2"},
                {"name": "Generate Spreadsheet", "link": "#", "icon": "file-text"},
            ]
        },
        {
            "name": "Student Management",
            "items": [
                {"name": "Manage Students", "link": "#", "icon": "users"},
                {"name": "Student Registration", "link": "#", "icon": "user-plus"},
                {"name": "Student List", "link": "#", "icon": "list"},
            ]
        },
        {
            "name": "Settings",
            "items": [
                {"name": "System Settings", "link": "#", "icon": "settings"},
                {"name": "User Profile", "link": "#", "icon": "user"},
                #{"name": "Log Out", "link": "#", "icon": "log-out"},
            ]
        },
    ]
    return render(request, 'pages/index.html', {'sidebar_menu': sidebar_menu, 'active_link': request.path})
