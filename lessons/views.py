from django.shortcuts import render
from django.http import HttpResponse
from lessons.forms import LogInForm



# Create your views here.


def login(request):
    form = LogInForm()
    return render(request, 'login.html',{'LogInForm':form})


def home(request):
    return render(request, 'home.html')

