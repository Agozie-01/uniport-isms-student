from django.urls import reverse

def sidebar_menu(request):
    sidebar_menu = [
        {
            "name": "Dashboard",
            "items": [
                {"name": "Overview", "link": reverse('home'), "icon": "grid"},  # Dashboard icon
            ],
        },
        {
            "name": "Management",
            "items": [
                {"name": "Results", "link": reverse('results_view'), "icon": "file-text"},  # Results icon
                {"name": "Students", "link": reverse('students_page'), "icon": "users"},  # students_page icon
                {"name": "Courses", "link": reverse('courses_page'), "icon": "book"},  # Sessions icon
                {"name": "Departments", "link": reverse('departments_page'), "icon": "layers"},  # Departments icon
                {"name": "Semesters", "link": reverse('semesters_page'), "icon": "calendar"},  # Semesters icon
                {"name": "Sessions", "link": reverse('sessions_page'), "icon": "clock"},  # Sessions icon
            ],
        },
        {
            "name": "Settings",
            "items": [
                {"name": "System", "link": reverse('settings_system'), "icon": "settings"},  # System settings icon
                {"name": "Profile", "link": reverse('settings_profile'), "icon": "user"},  # Profile icon
            ],
        },
    ]
    
    return {'sidebar_menu': sidebar_menu}
