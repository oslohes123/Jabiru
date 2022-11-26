from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.defaultfilters import lower

from .forms import LogInForm
from .forms import SignUpForm
from .forms import RequestForm
from .models import User


# Session parameter: useremail
# Gets you the email of the user that signed up or logged in
# To get user object call the getUser(request) and use .field_name to get your data

def login_user(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['useremail'] = request.user.email
                return redirect("dashboard")
            else:
                messages.add_message(request, messages.ERROR, "Invalid credentials try again")
        else:
            messages.add_message(request, messages.ERROR, "Invalid credentials try again")

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def outputStudentDashboard(request):
    return render(request,"Dashboards/student_dashboard.html")

def outputAdminDashboard(request):
    return render(request, "Dashboards/admin_dashboard.html")

def outputDirectorDashboard(request):
    return render(request, "Dashboards/director_dashboard.html")

# Each method should return a render
def dashboard(request):
    ourUser = getUser(request)
    if lower(ourUser.role) == "student":
        return outputStudentDashboard(request)
    elif lower(ourUser.role) == "admin":
        return outputAdminDashboard(request)
    elif lower(ourUser.role) == "director":
        return outputDirectorDashboard(request)
    else:
        print(f"Failed to find a user that fits the role:{ourUser.role}")
    
def make_request(request):
    form = RequestForm()
    return render(request, 'make_request.html', {'RequestForm':form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['useremail'] = request.user.email
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def getUser(request):
    try:
        return User.objects.get(email = request.session['useremail'])
    except User.DoesNotExist:
        emailRequest = request.session['useremail']
        return f'No user with this email {emailRequest}'
    except MultipleObjectsReturned:
        return "Multiple objects were returned"


def log_out(request):
    logout(request)
    return redirect('home')