from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.defaultfilters import lower
from django.contrib.auth.decorators import login_required
from .forms import LogInForm, SignUpForm, RequestForm
from .models import User
from .models import Lesson


# Session parameter: _
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
                request.session['user_email'] = request.user.email
                return redirect("dashboard")
            else:
                messages.add_message(request, messages.ERROR, "Invalid credentials try again")
        else:
            messages.add_message(request, messages.ERROR, "Invalid credentials try again")

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def output_student_dashboard(request):
    return render(request, "Dashboards/student_dashboard.html")


def output_admin_dashboard(request):
    return render(request, "Dashboards/administrator_dashboard.html")


def output_director_dashboard(request):
    return render(request, "Dashboards/director_dashboard.html")


# Each method should return a render
@login_required
def dashboard(request):
    ourUser = get_user(request, request.session["user_email"])
    if lower(ourUser.role) == "student":
        return output_student_dashboard(request)
    elif lower(ourUser.role) == "administrator":
        return output_admin_dashboard(request)
    elif lower(ourUser.role) == "director":
        return output_director_dashboard(request)
    else:
        print(f"Failed to find a user that fits the role:{ourUser.role}")
    messages.add_message(request, messages.ERROR, f"Failed to find a user that fits the role: {ourUser.role}")
    return redirect("login_user")


@login_required
def make_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Lesson.objects.create_lesson(get_user(request, request.session["user_email"]), data['availability'],
                                         data['lesson_numbers'], data['duration'], data['interval'],
                                         data['further_info'], False)
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully saved")

    insertForm = RequestForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': insertForm})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['user_email'] = request.user.email
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_required
def get_user(request, email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, f'No user with this email {email}')
        return User.DoesNotExist
    except MultipleObjectsReturned:
        messages.add_message(request, messages.ERROR, "Multiple objects were returned")
        return MultipleObjectsReturned


def get_requests(request):  # so far only works if a student email is inputted correctly
    student_lesson = request.GET
    student_email_query = student_lesson.get("student_email_input")
    try:
        userObject = get_user(request, student_email_query)
        if lower(userObject.role) != "student":
            messages.add_message(request, messages.ERROR, f"Email was not of a student, it was of a {userObject.role}")
            return output_admin_dashboard(request)
        else:
            lessons = Lesson.objects.filter(student=userObject)
            context = {"lessons": lessons}
            return render(request, "Dashboards/DashboardParts/student_lesson_search.html", context=context)
    except:
        return output_admin_dashboard(request)

def log_out(request):
    logout(request)
    return redirect('home')
