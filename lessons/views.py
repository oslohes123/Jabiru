from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .forms import LogInForm
from .forms import SignUpForm, AdministratorSignUpForm, AdministratorEditForm
from .forms import RequestForm, ApprovedBookingForm, InvoiceForm
from .models import User, Lesson, ApprovedBooking
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
    theUser = request.user
    lessonsdata = Lesson.objects.filter(student=theUser)
    approvedLessonData = ApprovedBooking.objects.filter(student=theUser)
    lessons_cost = total_lessons_cost(request, theUser.email)
    return render(request,"Dashboards/student_dashboard.html", {'lessonsdata':lessonsdata,'approvedLessonData':approvedLessonData
    , 'lessons_cost':lessons_cost})
    

def output_admin_dashboard(request):
    lessonsdata = Lesson.objects.all()
    approved_Lesson = ApprovedBooking.objects.all()
    return render(request, "Dashboards/administrator_dashboard.html" , {'approved_Lesson':approved_Lesson , 'lessonsdata':lessonsdata})



def output_director_dashboard(request):
    return render(request, "Dashboards/director_dashboard.html")


# Each method should return a render
@login_required
def dashboard(request):
    ourUser = get_user(request,request.session["user_email"])
    if ourUser.role == student:
        return output_student_dashboard(request)
    elif ourUser.role == administrator:
        return output_admin_dashboard(request)
    elif ourUser.role == director:
        return output_director_dashboard(request)
    else:
        print(f"Failed to find a user that fits the role:{ourUser.role}")
    messages.add_message(request, messages.ERROR, f"Failed to find a user that fits the role: {ourUser.role}")
    return redirect("login_user")



@login_required
@user_passes_test(lambda u: u.is_student,login_url='/dashboard/')
def make_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Lesson.objects.create_lesson(get_user(request, request.session["user_email"]), data['availability'],
                                         data['total_lessons_count'], data['duration'], data['interval'],
                                         data['further_info'], False)
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully saved")
    form = RequestForm()

    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': form})

def edit_unapproved_lessons(request, lesson_key): #Change info with primary key
    lesson = Lesson.objects.get(id = lesson_key)
    lesson_form = RequestForm(instance = lesson)
    if request.method == "POST":
        lesson_form = RequestForm(request.POST, instance= lesson)
        if lesson_form.is_valid():
            lesson_form.save()
            """ Lesson.objects.create_lesson(get_user(request, request.session["user_email"]), data['availability'],
                                         data['total_lessons_count'], data['duration'], data['interval'],
                                         data['further_info'], False) """
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully edited")

    context = {'RequestForm':lesson_form}
    return render(request, 'Dashboards/DashboardParts/make_request.html',context=context)


def approved_booking(request):
    if request.method == "POST":
        form = ApprovedBookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ApprovedBooking.objects.create_approvedBooking(get_user(request, request.session["user_email"]),data['start_date'],data['day_of_the_week'],data['total_lessons_count'],data['duration'],data['interval'],data['teacher'],data['price'],True)
            messages.add_message(request,messages.SUCCESS,"The lesson is successfully booked")

    form = ApprovedBookingForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'ApprovedBookingForm':form})

def make_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS, "The invoice is successfully updated")

    form = InvoiceForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': form})

# def edit_request(request, lesson_id):
#     request_to_edit = Lesson.objects.get(lesson_id=lesson_id)
#     if request.method == 'POST':
#         form = EditRequestForm(request.POST, instance=request_to_edit)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request,messages.SUCCESS, "The request is successfully edited")
#             return redirect('student_dashboard')
#     else:
#         form = EditRequestForm(instance=request_to_edit)
#     return render(request, 'edit_request.html', {'form': form})

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
@user_passes_test(lambda u: u.is_director,login_url='/dashboard/')
def sign_up_administrator(request):
    if request.method == 'POST':
        form = AdministratorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            # request.session['useremail'] = request.user.email
            messages.info(request, f'Administrator account {user.email} successfully created!')
            return redirect("dashboard")
    else:
        form = AdministratorSignUpForm()
    return render(request, 'sign_up_administrator.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_director,login_url='/dashboard/')
def delete_administrator(request, email):
    adminToDelete = User.objects.get(email=email)
    b = User.objects.filter(email=adminToDelete)
    b.delete()
    adminToDelete.delete()
    messages.info(request, f'The Administrator account {adminToDelete.email} has successfully been deleted!')
    return redirect('view_all_administrators')

@login_required
@user_passes_test(lambda u: u.is_director,login_url='/dashboard/')
def edit_administrator(request, email):
    adminToEdit = User.objects.get(email=email)
    if request.method == 'POST':
        form = AdministratorEditForm(request.POST, instance=adminToEdit)
        if form.is_valid():
            form.save()
            messages.info(request, f'The Administrator account details of {adminToEdit.email} has been successfully edited!')
            return redirect('view_all_administrators')
    else:
        form = AdministratorEditForm(instance=adminToEdit)
    return render(request, 'edit_administrator.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_director,login_url='/dashboard/')
def make_super_administrator(request, email):
    adminToPromote = User.objects.get(email=email)
    adminToPromote.role = director
    adminToPromote.save()
    messages.info(request, f'The Administrator account {adminToPromote} is now a Director!')
    return redirect('view_all_administrators')
    
        
@login_required
@user_passes_test(lambda u: u.is_director,login_url='/dashboard/')
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
@user_passes_test(lambda u: u.is_director_or_administrator,login_url='/dashboard/')
def get_requests(request):  # so far only works if a student email is inputted correctly
    student_lesson = request.GET
    student_email_query = student_lesson.get("student_email_input")
    try:
        user_object = get_user(request, student_email_query)
        if user_object.role != student:
            messages.add_message(request, messages.ERROR, f"Email was not of a student, it was of a {user_object.role}")
            return output_admin_dashboard(request)
        else:
            costs = total_lessons_cost(request, user_object.email)
            lessons = Lesson.objects.filter(student=user_object)
            context = {"lessons": lessons, 'lessons_cost':costs}
            return render(request, "Dashboards/DashboardParts/student_lesson_search.html", context=context)
    except:
        return output_admin_dashboard(request)

@login_required
def getLessons(request):
    lessons = Lesson.objects.all()
    return lessons


def log_out(request):
    logout(request) 
    return redirect('home')


def delete_request(request, lesson_key):
    lesson = Lesson.objects.get(id = lesson_key)
    lesson.delete()
    return redirect('/dashboard/')

def total_lessons_cost(request,email): #get the total price of each lesson that the student has
    student_object = get_user(request,email)
    if student_object.role != student:
        messages.add_message(request, messages.ERROR, f"Email was not of a student, it was of a {student_object.role}")
    else:
        lessons =  ApprovedBooking.objects.filter(student=student_object)
        #for loop to go through each lesson and getting total price add em all up
        total_cost = 0 #TODO: change to maybe students actual balance as for now its always going to be 0
        for i in lessons:
            total_cost -= i.total_price()
        return total_cost