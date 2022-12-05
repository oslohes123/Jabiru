"""Tests of the editing administrator view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import AdministratorEditForm
from lessons.models import User

class EditAdministratorViewTestCase(TestCase):
    """Tests of the editing administrator view."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = 'http://localhost:8000/edit_administrator/(%3FPjanedoe@example.org%5Cd+)'
        self.directorUser = User.objects.get(email='petrapickles@example.org')
        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }
        login_url = reverse("login_user")
        self.dashboard = self.client.post(login_url,self.directorForm,follow=True)
        administrator_list_url = reverse('view_all_administrators')
        self.administrator_list = self.client.post(administrator_list_url, follow=True)
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'changedemail@example.org',
            'password': 'Password123%',
            'confirm_password': 'Password123%'
        }
        self.adminUser = User.objects.get(email='janedoe@example.org')
        self.adminForm = {
            "email": "janedoe@example.org",
            "password": "Password123%"
        }

    def test_start_from_administrator_list(self):
        self.assertTemplateUsed(self.administrator_list, 'Dashboards/DashboardParts/AdministratorParts/view_all_administrators.html')

    def test_sign_up_url(self):
        self.assertEqual(self.url, 'http://localhost:8000/edit_administrator/(%3FPjanedoe@example.org%5Cd+)')
 
    def test_get_edit_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_administrator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdministratorEditForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_edit(self):
        self.form_input['email'] = 'bademail'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/AdministratorParts/edit_administrator.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdministratorEditForm))
        self.assertTrue(form.is_bound)
        self.assertTrue(self._is_logged_in())

    def test_successful_edit(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('view_all_administrators')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/AdministratorParts/view_all_administrators.html')
        user = User.objects.get(email='changedemail@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_correct = check_password('Password123%', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())