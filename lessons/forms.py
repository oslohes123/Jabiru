from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import RegexValidator
from .models import User, Lesson, ApprovedBooking, Invoice
from lessons.constants import *


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$&+,:;=?@#|<>.^*()%!-]).*$',
                message='Password must contain an uppercase character, a lowercase character, a number and a special character.')
        ]
    )
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['last_name'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['email'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['password'].widget.attrs['class'] = 'form-control mt-2'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control mt-2'

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
            role=student,
        )
        return user


class AdministratorSignUpForm(SignUpForm):
    def save(self):
        forms.ModelForm.save(self, commit=False)
        user = User.objects.create_user(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
            role=administrator,
        )
        return user


class AdministratorEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$&+,:;=?@#|<>.^*()%!-]).*$',
                message='Password must contain an uppercase character, a lowercase character, a number and a special character.')
        ]
    )
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class RequestForm(forms.ModelForm):
    # total_lessons_count = forms.IntegerField(label="Number of lessons")
    # interval = forms.IntegerField(label="Interval (0-8)", max_value=8, min_value=0)
    # duration = forms.IntegerField(label="Duration(0-240)", max_value=240, min_value=0)
    class Meta:
        model = Lesson
        fields = ['availability', 'total_lessons_count', 'duration', 'interval', 'further_info']
        widgets = {'availability': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'style': 'resize:none;'}),
                   'further_info': forms.Textarea(attrs={'rows': 10, 'cols': 60, 'style': 'resize:none;'})}


    field_order = ['availability', 'total_lessons_count', 'duration', 'interval', 'further_info']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['total_lessons_count'].widget.attrs['class'] = 'form-control'
        self.fields['availability'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['interval'].widget.attrs['class'] = 'form-control'
        self.fields['further_info'].widget.attrs['class'] = 'form-control'


class ApprovedBookingForm(forms.ModelForm):
    start_date = forms.DateField(label="start date")
    day_of_the_week = forms.CharField(label="day of the week")
    time_of_the_week = forms.TimeField(label="time of the week")
    total_lessons_count = forms.IntegerField(label="total number of lessons", min_value=0)

    class Meta:
        model = ApprovedBooking
        fields = ['duration', 'interval', 'assigned_teacher', 'hourly_rate']
        fields_order = ['start_date', 'day_of_the_week', 'time_of_the_week', 'total_lessons_count', 'duration', 'interval', 'assigned_teacher', 'hourly_rate']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'form-control'
        self.fields['day_of_the_week'].widget.attrs['class'] = 'form-control'
        self.fields['time_of_the_week'].widget.attrs['class'] = 'form-control'
        self.fields['total_lessons_count'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['interval'].widget.attrs['class'] = 'form-control'
        self.fields['assigned_teacher'].widget.attrs['class'] = 'form-control'
        self.fields['hourly_rate'].widget.attrs['class'] = 'form-control'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['lesson_in_invoice', 'balance_due', 'payment_paid']

    def save(self):
        invoice = super().save(commit=False)

        return invoice

