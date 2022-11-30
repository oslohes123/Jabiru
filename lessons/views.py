from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.defaultfilters import lower
from django.contrib.auth.decorators import login_required

from .forms import LogInForm
from .forms import SignUpForm, AdministratorSignUpForm, AdministratorEditForm
from .forms import RequestForm
from .models import User, Lesson
from django.views import generic


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

def outputAdministratorDashboard(request):
    return render(request, "Dashboards/administrator_dashboard.html")

def outputDirectorDashboard(request):
    return render(request, "Dashboards/director_dashboard.html")

# Each method should return a render
@login_required
def dashboard(request):
    ourUser = getUser(request)
    if lower(ourUser.role) == "student":
        return outputStudentDashboard(request)
    elif lower(ourUser.role) == "administrator":
        return outputAdministratorDashboard(request)
    elif lower(ourUser.role) == "director":
        return outputDirectorDashboard(request)
    else:
        messages.add_message(request,messages.ERROR,f"Failed to find a user that fits the role: {ourUser.role}")
        return redirect("login_user")

@login_required
def make_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Lesson.objects.create_lesson(getUser(request),data['availability'],data['lesson_numbers'],data['duration'],data['interval'],data['further_info'],False)
            messages.add_message(request,messages.SUCCESS,"The lesson has been successfully saved")

    insertForm = RequestForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm':insertForm})

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

@login_required
def sign_up_administrator(request):
    if request.method == 'POST':
        form = AdministratorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            # request.session['useremail'] = request.user.email
            messages.info(request, 'Administrator account successfully created!')
            return redirect("dashboard")
    else:
        form = AdministratorSignUpForm()
    return render(request, 'sign_up_administrator.html', {'form': form})

@login_required
def delete_administrator(request, email):
    adminToDelete = User.objects.get(email=email)
    b = User.objects.filter(email=adminToDelete)
    b.delete()
    adminToDelete.delete()
    messages.info(request, 'Administrator account successfully deleted!')
    return redirect('view_all_administrators')

@login_required
def edit_administrator(request, email):
    adminToEdit = User.objects.get(email=email)
    if request.method == 'POST':
        form = AdministratorEditForm(request.POST, instance=adminToEdit)
        if form.is_valid():
            form.save()
            messages.info(request, 'The Administrator account has been successfully edited!')
            return redirect('view_all_administrators')
    else:
        form = AdministratorEditForm(instance=adminToEdit)
    return render(request, 'edit_administrator.html', {'form': form})
        

@login_required
def view_all_administrators(request):
    administrators = User.objects.filter(role="Administrator")
    return render(request, 'view_all_administrators.html', {'administrators': administrators})

@login_required
def getUser(request):
    try:
        return User.objects.get(email = request.session['useremail'])
    except User.DoesNotExist:
        emailRequest = request.session['useremail']
        return f'No user with this email {emailRequest}'
    except MultipleObjectsReturned:
        return "Multiple objects were returned"


@login_required
def getLessons(request):
    lessons = Lesson.objects.all()
    return lessons


def log_out(request):
    logout(request)
    return redirect('home')