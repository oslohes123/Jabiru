from django.test import TestCase
from lessons.forms import LogInForm;

class LogInUserTestForm(TestCase):
    """Unit tests for logging in a user"""
    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email',form.fields)
        self.assertIn('password',form.fields)

        
