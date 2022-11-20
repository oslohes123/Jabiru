from django import forms
from django.core.validators import RegexValidator
from .models import User, Lesson

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

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""
    class Meta:
        model = User
        fields = ['email']
        
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class RequestForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['availability', 'lesson_numbers', 'duration', 'interval', 'further_info']
        widgets = { 'availability': forms.Textarea(attrs={'rows':6, 'cols':60}), 'further_info':forms.Textarea(attrs={'rows':10, 'cols':60}) }


