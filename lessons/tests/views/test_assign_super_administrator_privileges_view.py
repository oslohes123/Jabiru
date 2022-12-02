"""Tests of the assigning super-administrator privileges view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import AdministratorEditForm
from lessons.models import User

class AssignSuperAdministratorViewTestCase(TestCase):
    """Tests of the assigning super-administrator privileges view."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = 'http://localhost:8000/make_super_administrator/(%3FPjanedoe@example.org%5Cd+)'
        self.directorUser = User.objects.get(email='petrapickles@example.org')
        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }
        login_url = reverse("login_user")
        self.dashboard = self.client.post(login_url,self.directorForm,follow=True)
        administrator_list_url = reverse('view_all_administrators')
        self.administrator_list = self.client.post(administrator_list_url, follow=True)
        

    def test_start_from_administrator_list(self):
        self.assertTemplateUsed(self.administrator_list, 'view_all_administrators.html')

    def test_sign_up_url(self):
        self.assertEqual(self.url,'http://localhost:8000/make_super_administrator/(%3FPjanedoe@example.org%5Cd+)')

    def test_assign_super_administrator(self):
        adminUser = User.objects.get(email='janedoe@example.org')
        self.assertEqual(adminUser.role, 'Administrator')
        before_count = User.objects.count()
        response = self.client.post(self.url, follow=True)
        response_url = reverse('view_all_administrators')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        promotedUser = User.objects.get(email='janedoe@example.org')
        self.assertEqual(promotedUser.role, 'Director')