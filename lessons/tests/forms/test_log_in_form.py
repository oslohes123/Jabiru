from django import forms
from django.test import TestCase
from lessons.forms import LogInForm

class LogInUserTestForm(TestCase):
    def setUp(self):
        self.formInput = {"email":"testing@email.com","password":"Testing123%"}

    """Unit tests for logging in a user"""
    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email',form.fields)
        self.assertIn('password',form.fields)
        password_field = form.fields["password"]
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.formInput)
        self.assertTrue(form.is_valid())


        
