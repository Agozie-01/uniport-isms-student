from django.shortcuts import render
from django.urls import reverse
from adminapp.models import Test

def dashboard_home(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/index.html', {'active_link': request.path})


def dashboard_upload_results(request):
    # Define the sidebar menu with groups and items
    return render(request, 'pages/results_upload.html', {'active_link': request.path})
