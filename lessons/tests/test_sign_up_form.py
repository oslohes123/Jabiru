from django.test import TestCase
from django import forms
from lessons.forms import SignUpForm
from lessons.models import User

class SignUpFormTestCase(TestCase):
    """Sign up form unit tests"""


    def setUp(self):
        self.form_input = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'namelastname@example.org',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }
    #Accept valid input data
    def test_valid_data_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_necessary_fields_in_sign_up_form(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

        self.assertIn('password', form.fields)
        pass_widget = form.fields['password'].widget
        self.assertTrue(isinstance(pass_widget, forms.PasswordInput))

        self.assertIn('confirm_password', form.fields)
        confirm_pass_widget = form.fields['confirm_password'].widget
        self.assertTrue(isinstance(confirm_pass_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'bademail'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase(self):
        self.form_input['password'] = 'password123!'
        self.form_input['confirm_password'] = 'password123!'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase(self):
        self.form_input['password'] = 'PASSWORD123!'
        self.form_input['confirm_password'] = 'PASSWORD123!'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['password'] = 'Password!'
        self.form_input['confirm_password'] = 'Password!'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_special_char(self):
        self.form_input['password'] = 'Password123'
        self.form_input['confirm_password'] = 'Password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_match(self):
        self.form_input['password'] = 'Password123!'
        self.form_input['confirm_password'] = 'WrongPassword123!'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())