from django import forms;
from django.core.validators import RegexValidator

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


