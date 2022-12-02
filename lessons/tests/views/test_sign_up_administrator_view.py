"""Tests of the signing up a new administrator view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import AdministratorSignUpForm
from lessons.models import User

class SignUpAdministratorViewTestCase(TestCase):
    """Tests of the signing up a new administrator view."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = reverse('sign_up_administrator')
        self.directorUser = User.objects.get(email='petrapickles@example.org')
        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }
        login_url = reverse("login_user")
        self.dashboard = self.client.post(login_url,self.directorForm,follow=True)
        self.form_input = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'namelastname@example.org',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }

    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/director_dashboard.html')

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up_administrator/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up_administrator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdministratorSignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = 'bademail'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up_administrator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdministratorSignUpForm))
        self.assertTrue(form.is_bound)
        self.assertTrue(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'Dashboards/director_dashboard.html')
        user = User.objects.get(email='namelastname@example.org')
        self.assertEqual(user.first_name, 'Name')
        self.assertEqual(user.last_name, 'Lastname')
        is_password_correct = check_password('Password123!', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
