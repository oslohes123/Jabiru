import decimal
from datetime import date, datetime

from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from decimal import Decimal
from .forms import *
from .models import User, Lesson, ApprovedBooking, Invoice
from django.views import generic
from .constants import *


# Session parameter: _
# Gets you the email of the user that signed up or logged in
# To get user object call the getUser(request) and use .field_name to get your data

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
    approvedLessonData = ApprovedBooking.objects.filter(student=theUser)

    data = []
    for i in approvedLessonData:
        data_item = {"lesson": i,
                     "invoice": Invoice.objects.get(lesson_in_invoice=i)
                     }
        data.append(data_item)

    return render(request, "Dashboards/student_dashboard.html",
                  {'data': data,'lessonsdata':lessonsdata})


# TODO: Arraf replace balance due next to total_price with your function to get the price for the user.
def return_invoice_for_approved(request):
    if request.method == "POST":
        query = request.POST
        approved_booking_object = ApprovedBooking.objects.get(id=query.get('lesson_id'))
        invoice = Invoice.objects.get(lesson_in_invoice=approved_booking_object)
        invoice = {
            "invoice_num": '{0:03}'.format(invoice.pk),
            "student_ref_num": '{0:03}'.format(approved_booking_object.student.pk),
            "total_price": invoice.balance_due
        }
        return render(request, "Dashboards/DashboardParts/Invoice.html", {'invoice': invoice})
    else:
        messages.add_message(request, messages.ERROR, "You can't go here")
        redirect("dashboard")


@login_required
def make_payment_approved_lesson(request):
    if request.method == "POST":
        query = request.POST
        if query.get('making_payment') == "False":
            lesson_id = query.get('lesson_id')
            payment_form = TransactionForm()
            return render(request, "Dashboards/DashboardParts/make_payment.html",
                          {'lesson_id': lesson_id, 'form': payment_form})
        else:
            lesson_id = query.get("lesson_id")
            approved_booking = ApprovedBooking.objects.get(id=lesson_id)
            our_invoice = Invoice.objects.get(lesson_in_invoice=approved_booking)
            payment_amount = query.get("payment_amount")
            payment_amount = decimal.Decimal(payment_amount)
            Transaction.objects.create_transaction(our_invoice, payment_amount)
            our_invoice.balance_due = our_invoice.balance_due - payment_amount
            our_invoice.save()

            return redirect("dashboard")
    else:
        return redirect("dashboard")


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
    else:
        user_to_assign = request.user

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Lesson.objects.create_lesson(user_to_assign, data['availability'],
                                         data['total_lessons_count'], data['duration'], data['interval'],
                                         data['further_info'], False)
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully saved")
            return redirect("dashboard")
        else:
            messages.add_message(request, messages.ERROR, "The form submitted is not valid try again")
    form = RequestForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': form})


@login_required
@user_passes_test(lambda u: u.is_adult, login_url='/dashboard/')
def make_request_for_child(request):
    form_input_query_dict = request.POST
    child_id = form_input_query_dict.get("child_id")
    request.session["child_id"] = child_id
    insertForm = RequestForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': insertForm})


@login_required
def edit_unapproved_lessons(request):
    if request.method == "POST":
        query = request.POST
        lesson_id = query.get("lesson_id")
        lesson = Lesson.objects.get(id=lesson_id)
        lesson_form = RequestForm(request.POST, instance=lesson)
        if lesson_form.is_valid():
            lesson_form.save()
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully edited")
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Invalid details, try again")
            lesson_form = RequestForm(instance=lesson)
            return render(request, 'Dashboards/DashboardParts/edit_request.html',
                          {'RequestForm': lesson_form, 'lesson_id': lesson_id})
    else:
        return redirect('dashboard')


@login_required
def fill_edit_unapproved_lessons(request):
    if request.method == "POST":
        query = request.POST
        lesson_id = query.get("lesson_id")
        print("lessssun")
        print(lesson_id)
        lesson_obj = Lesson.objects.get(id=lesson_id)
        form = RequestForm(instance=lesson_obj)
        return render(request, 'Dashboards/DashboardParts/edit_request.html',
                      {'RequestForm': form, 'lesson_id': lesson_id})
    else:
        return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_director_or_administrator, login_url='/dashboard/')
def approve_request(request):
    if request.method == "POST":
        query = request.POST
        student_id = query.get("student_id")
        lesson_id = query.get("lesson_id")
        student_obj = User.objects.get(id=student_id)
        lesson_obj = Lesson.objects.get(id=lesson_id)
        form = ApprovedBookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            approved_lesson = ApprovedBooking.objects.create_approvedBooking(student_obj, data['start_date'],
                                                                             data['day_of_the_week'],
                                                                             data['time_of_the_week'],
                                                                             data['total_lessons_count'],
                                                                             data['duration'], data['interval'],
                                                                             data['assigned_teacher'],
                                                                             data['hourly_rate'])
            Invoice.objects.create_invoice(lesson_in_invoice=approved_lesson, balance_due=approved_lesson.total_price())
            messages.add_message(request, messages.SUCCESS, "The lesson has been successfully approved")
            lesson_obj.approve_status = True
            lesson_obj.save()
            return redirect("dashboard")
        else:
            messages.add_message(request, messages.ERROR, "Invalid details, try again")
            return render(request, 'Dashboards/DashboardParts/approve_request.html',
                          {'ApprovedBookingForm': form, 'student_id': student_id, 'lesson_id': lesson_id})
    else:
        return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_director_or_administrator, login_url='/dashboard/')
def fill_in_approve_request(request):
    if request.method == "POST":
        query = request.POST
        lesson_id = query.get("lesson_request")
        student_id = query.get("student")
        lesson = Lesson.objects.get(id=lesson_id)
        data_dict = {'start_date': date.today(), 'time_of_the_week': datetime.now(),
                     'total_lessons_count': lesson.total_lessons_count,
                     'duration': lesson.duration, 'interval': lesson.interval, 'assigned_teacher': lesson.further_info}
        form = ApprovedBookingForm(initial=data_dict)
        return render(request, 'Dashboards/DashboardParts/approve_request.html',
                      {'ApprovedBookingForm': form, 'student_id': student_id, 'lesson_id': lesson_id})
    else:
        return redirect('dashboard')


def make_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The invoice is successfully updated")

    form = InvoiceForm()
    return render(request, 'Dashboards/DashboardParts/make_request.html', {'RequestForm': form})


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def sign_up_administrator(request):
    if request.method == 'POST':
        form = AdministratorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(request, messages.SUCCESS, f'Administrator account {user.email} successfully created!')
            return redirect("dashboard")
    else:
        form = AdministratorSignUpForm()
    return render(request, 'Dashboards/DashboardParts/AdministratorParts/sign_up_administrator.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def delete_administrator(request):
    if request.method == "POST":
        query = request.POST
        email = query.get("email")
        adminToDelete = User.objects.get(email=email)
        b = User.objects.filter(email=adminToDelete)
        b.delete()
        adminToDelete.delete()
        messages.add_message(request, messages.SUCCESS,
                             f'The Administrator account {adminToDelete.email} has successfully been deleted!')
        return redirect('view_all_administrators')
    else:
        return redirect('view_all_administrators')


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def edit_administrator(request):
    if request.method == 'POST':
        query = request.POST
        email = query.get("email")
        adminToEdit = User.objects.get(email=email)
        form = AdministratorEditForm(request.POST, instance=adminToEdit)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 f'The Administrator account details of {adminToEdit.email} has been successfully '
                                 f'edited!')
            return redirect('view_all_administrators')
        else:
            messages.add_message(request, messages.ERROR, "Invalid attempt, please enter valid details")
            form = AdministratorEditForm(instance=adminToEdit)
            return render(request, 'Dashboards/DashboardParts/AdministratorParts/edit_administrator.html',
                          {'form': form, 'email': email})
    else:
        return redirect('view_all_administrators')


def fill_edit_administrator(request):
    if request.method == "POST":
        query = request.POST
        email = query.get("email")
        adminToEdit = User.objects.get(email=email)
        form = AdministratorEditForm(instance=adminToEdit)
        return render(request, 'Dashboards/DashboardParts/AdministratorParts/edit_administrator.html',
                      {'form': form, 'email': email})
    else:
        return redirect('view_all_administrators')


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def make_super_administrator(request):
    if request.method == "POST":
        query = request.POST
        email = query.get("email")
        adminToPromote = User.objects.get(email=email)
        adminToPromote.role = director
        adminToPromote.save()
        messages.add_message(request, messages.SUCCESS,
                             f'The Administrator account {adminToPromote} is now a Director!')
        return redirect('view_all_administrators')
    else:
        return redirect('view_all_administrators')


@login_required
@user_passes_test(lambda u: u.is_director, login_url='/dashboard/')
def view_all_administrators(request):
    administrators = User.objects.filter(role="Administrator")
    return render(request, 'Dashboards/DashboardParts/AdministratorParts/view_all_administrators.html',
                  {'administrators': administrators})


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
    student_lesson = request.POST
    student_email_query = student_lesson.get("student_email_input")
    try:
        user_object = get_user(request, student_email_query)
        if user_object.role != student:
            messages.add_message(request, messages.ERROR, f"Email was not of a student, it was of a {user_object.role}")
            return output_admin_dashboard(request)
        else:
            lessons = Lesson.objects.filter(student=user_object)
            context = {"lessons": lessons, "student": user_object}
            return render(request, "Dashboards/DashboardParts/student_lesson_search.html", context=context)
    except:
        return output_admin_dashboard(request)


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


@login_required
def delete_request(request):
    if request.method == "POST":
        query = request.POST
        lesson_key = query.get("lesson_id")
        lesson = Lesson.objects.get(id=lesson_key)
        lesson.delete()
        return redirect('dashboard')
    else:
        return redirect('dashboard')
