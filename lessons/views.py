from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .forms import LogInForm
from .forms import SignUpForm, AdministratorSignUpForm, AdministratorEditForm
from .forms import RequestForm
from .models import User, Lesson
from django.views import generic
from .constants import *


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
                request.session["child_id"] = None
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
    theUser = request.user
    lessonsdata = Lesson.objects.filter(student=theUser)
    return render(request, "Dashboards/student_dashboard.html", {'lessonsdata': lessonsdata})


def output_adult_dashboard(request):
    theUser = request.user
    lessonsdata = Lesson.objects.filter(student=theUser)
    childdata = theUser.children.all()
    return render(request, "Dashboards/adult_dashboard.html", {'lessonsdata': lessonsdata, 'childdata': childdata})


def output_admin_dashboard(request):
    return render(request, "Dashboards/administrator_dashboard.html")


def output_director_dashboard(request):
    return render(request, "Dashboards/director_dashboard.html")


# Each method should return a render
@login_required
def dashboard(request):
    ourUser: User = request.user
    if ourUser.role == student:
        return output_student_dashboard(request)
    if ourUser.role == adult:
        return output_adult_dashboard(request)
    elif ourUser.role == administrator:
        return output_admin_dashboard(request)
    elif ourUser.role == director:
        return output_director_dashboard(request)
    else:
        print(f"Failed to find a user that fits the role:{ourUser.role}")
    messages.add_message(request, messages.ERROR, f"Failed to find a user that fits the role: {ourUser.role}")
    return redirect("login_user")


@login_required
@user_passes_test(lambda u: u.is_student_or_adult, login_url='/dashboard/')
def make_request(request):
    if request.session["child_id"] is not None:
        user_to_assign = User.objects.get(id=request.session["child_id"])
        request.session["child_id"] = None
        print(f"Assigning child {user_to_assign.email}")
    else:
        user_to_assign = request.user
        print(f"Assigning parent {user_to_assign.email}")

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Lesson.objects.create_lesson(user_to_assign, data['availability'],
                                         data['lesson_numbers'], data['duration'], data['interval'],
                                         data['further_info'], False)
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully saved")

    insertForm = RequestForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': insertForm})


# child_id_global = None

@login_required
@user_passes_test(lambda u: u.is_adult, login_url='/dashboard/')
def make_request_for_child(request, child_id):
    # child = User.objects.get(id=child_id)
    # print(child.email)
    # if request.method == "POST":
    #     form = RequestForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         Lesson.objects.create_lesson(child, data['availability'],
    #                                      data['lesson_numbers'], data['duration'], data['interval'],
    #                                      data['further_info'], False)
    #         messages.add_message(request, messages.SUCCESS, "The lesson has been successfully saved")
    # global child_id_global
    # child_id_global = child_id
    request.session["child_id"] = child_id
    insertForm = RequestForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': insertForm})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session["child_id"] = None
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
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
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def delete_administrator(request, email):
    adminToDelete = User.objects.get(email=email)
    b = User.objects.filter(email=adminToDelete)
    b.delete()
    adminToDelete.delete()
    messages.info(request, 'Administrator account successfully deleted!')
    return redirect('view_all_administrators')


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
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
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def view_all_administrators(request):
    administrators = User.objects.filter(role="Administrator")
    return render(request, 'view_all_administrators.html', {'administrators': administrators})


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


@login_required
@user_passes_test(lambda u: u.is_director_or_administrator, login_url='/dashboard/')
def get_requests(request):  # so far only works if a student email is inputted correctly
    student_lesson = request.GET
    student_email_query = student_lesson.get("student_email_input")
    try:
        user_object = get_user(request, student_email_query)
        if user_object.role != student:
            messages.add_message(request, messages.ERROR, f"Email was not of a student, it was of a {user_object.role}")
            return output_admin_dashboard(request)
        else:
            lessons = Lesson.objects.filter(student=user_object)
            context = {"lessons": lessons}
            return render(request, "Dashboards/DashboardParts/student_lesson_search.html", context=context)
    except:
        return output_admin_dashboard(request)


@login_required
def getLessons(request):
    lessons = Lesson.objects.all()
    return lessons


@login_required
@user_passes_test(lambda u: u.is_adult, login_url='/dashboard/')
def assign_child(request):
    theUser = request.user
    if request.method == "POST":
        form_input_query_dict = request.POST
        child_email = form_input_query_dict.get("student_email_input")
        try:
            child_object = get_user(request, child_email)
            if child_object.role != student:
                messages.add_message(request, messages.ERROR,
                                     f"Email was not of a student, it was of a {child_object.role}")
                return render(request, "assign_child.html")
            else:
                child_object.parent = theUser
                child_object.save()
                messages.add_message(request, messages.SUCCESS,
                                     f"Your child has been successfully assigned to you")
                return render(request, "assign_child.html")
        except:
            return render(request, "assign_child.html")
    else:
        return render(request, "assign_child.html")


def log_out(request):
    logout(request)
    return redirect('home')
