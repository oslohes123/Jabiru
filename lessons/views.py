from django.shortcuts import render
from django.http import HttpResponse
from .forms import LogInForm
from .forms import SignUpForm

def sign_up(request):
    form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def login(request):
    form = LogInForm()
    return render(request, 'login.html',{'LogInForm':form})

def home(request):
    return render(request, 'home.html')
