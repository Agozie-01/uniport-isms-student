from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from adminapp.models import Test

def dashboard_view(request):
    greeting = "Good morning friends"
    data = Test.objects.all()
    return render(request, 'pages/index.html', {"greeting": greeting, "data": data})

