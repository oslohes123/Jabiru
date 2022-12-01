from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import RegexValidator
from .models import User, Lesson, ApprovedBooking

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
            role = "Student",
        )
        return user

class AdministratorSignUpForm(forms.ModelForm):
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

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
            role = "Administrator",
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

class RequestForm(forms.ModelForm):
    lesson_numbers = forms.IntegerField(label="number of lessons")
    class Meta:
        model = Lesson
        fields = ['availability','duration','interval','further_info']
        widgets = {'availability': forms.Textarea(attrs={'rows':6, 'cols':60, 'style':'resize:none;'}), 'further_info':forms.Textarea(attrs={'rows':10, 'cols':60, 'style':'resize:none;'}) }
        fields_order = ['availability','lesson_numbers','duration','interval','further_info']

    def save(self):
        super().save(commit=False)
        lesson = Lesson.objects.create_lesson(
            availability = self.cleaned_data.get('availability'),
            lesson_numbers = self.cleaned_data.get('lesson_numbers'),
            duration = self.cleaned_data.get('duration'),
            interval = self.cleaned_data.get('interval'),
            further_info = self.cleaned_data.get('further_info')
        )
        return lesson

class ApprovedBookingForm(forms.ModelForm):
    start_date = forms.DateField(label="start date")
    day_of_the_week = forms.DateTimeField(label="day and time of the week")
    lesson_numbers = forms.IntegerField(label="number of lessons")
    class Meta:
        model = ApprovedBooking
        fields = ['duration','interval','teacher']
        fields_order = ['start_date','day_of_the_week','lesson_numbers','duration','interval','teacher']
    
    def save(self):
        super().save(commit=False)
        approvedBooking = ApprovedBooking.objects.create_approvedBooking(
            start_date = self.cleaned_data.get('start_date'),
            day_of_the_week = self.cleaned_data.get('day_of_the_week'),
            lesson_numbers = self.cleaned_data.get('lesson_numbers'),
            duration = self.cleaned_data.get('duration'),
            interval = self.cleaned_data.get('interval'),
            teacher = self.cleaned_data.get('teacher'),
        )
        return approvedBooking

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['invoice_num', 'total_price']

