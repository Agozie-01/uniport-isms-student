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
