from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import RegexValidator
from .models import User, Lesson


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
        labels = {'role': 'Select account type'}

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
        self.fields['role'].widget.attrs['class'] = 'form-control mt-2'
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
            role="Student",
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
            role="Administrator",
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
    interval = forms.IntegerField(label="Interval (0-8)", max_value=8, min_value=0)
    duration = forms.IntegerField(label="Duration(0-240)", max_value=240, min_value=0)
    lesson_numbers = forms.IntegerField(label="Number of lessons")

    class Meta:
        model = Lesson
        fields = ['availability', 'further_info']
        widgets = {'availability': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
                   'further_info': forms.Textarea(attrs={'rows': 10, 'cols': 60})}

    field_order = ['availability', 'lesson_numbers', 'duration', 'interval', 'further_info']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['availability'].widget.attrs['class'] = 'form-control'
        self.fields['lesson_numbers'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['interval'].widget.attrs['class'] = 'form-control'
        self.fields['further_info'].widget.attrs['class'] = 'form-control'
