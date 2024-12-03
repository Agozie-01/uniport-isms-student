from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from api.models import Test

def login_view(request):
    greeting = "Good morning friends"
    data = Test.objects.all()
    return render(request, 'pages/login.html', {"greeting": greeting, "data": data})

    