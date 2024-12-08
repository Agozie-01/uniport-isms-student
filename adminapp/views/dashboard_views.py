from django.shortcuts import render
from django.urls import reverse
from api.models import Test

def home(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/index.html', {'active_link': request.path})


def results(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/results.html', {'active_link': request.path})

def students(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/students.html', {'active_link': request.path})

def sessions(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/sessions.html', {'active_link': request.path})

def semesters(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/semesters.html', {'active_link': request.path})

def departments(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/departments.html', {'active_link': request.path})

def courses(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/courses.html', {'active_link': request.path})
