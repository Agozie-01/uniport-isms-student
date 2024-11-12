from django.shortcuts import render

from adminapp.models import Test

def home(request):
    greeting = "Good morning friends"
    data = Test.objects.all()
    return render(request, 'index.html', {"greeting": greeting, "data": data})
