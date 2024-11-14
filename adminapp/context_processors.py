from django.urls import reverse

def sidebar_menu(request):
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
                {"name": "Upload Results", "link": reverse('results_upload'), "icon": "upload"},
                {"name": "View Results", "link": reverse('results_view'), "icon": "eye"},
                {"name": "Result Analysis", "link": reverse('results_analysis'), "icon": "bar-chart-2"},
                {"name": "Generate Spreadsheet", "link": reverse('results_spreadsheet_generate'), "icon": "file-text"},
            ]
        },
        {
            "name": "Student Management",
            "items": [
                {"name": "Manage Students", "link": reverse('students_manage'), "icon": "users"},
                {"name": "Student Registration", "link": reverse('student_registration'), "icon": "user-plus"},
                {"name": "Student List", "link": reverse('students'), "icon": "list"},
            ]
        },
        {
            "name": "Settings",
            "items": [
                {"name": "System Settings", "link": reverse('settings_system'), "icon": "settings"},
                {"name": "User Profile", "link": reverse('settings_profile'), "icon": "user"},
                #{"name": "Log Out", "link": "#", "icon": "log-out"},
            ]
        },
    ]
    
    return {'sidebar_menu': sidebar_menu}
