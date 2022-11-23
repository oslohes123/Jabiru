from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LogInForm
from .forms import SignUpForm
from .forms import RequestForm


# TODO: For landing page put the name of the view(from urls.py) as the redirect_url
def login_user(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = "" # Upcoming landingPage name needs to be insertedHere
                return redirect(redirect_url)
            else:
                messages.add_message(request, messages.ERROR, "Invalid credentials try again")
        else:
            messages.add_message(request, messages.ERROR, "Invalid credentials try again")

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def tempLandingPage(request):
    return render(request,"tempLandingPage.html")
    
def make_request(request):
    form = RequestForm()
    return render(request, 'make_request.html', {'RequestForm':form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('LANDINGPAGE')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
