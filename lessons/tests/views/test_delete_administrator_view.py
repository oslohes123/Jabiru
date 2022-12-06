"""Tests of the deleting administrator view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User

class DeleteAdministratorViewTestCase(TestCase):
    """Tests of the deleting administrator view."""

    fixtures = ['lessons/fixtures/user.json']

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = reverse('delete_administrator')
        self.directorUser = User.objects.get(email='petrapickles@example.org')
        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }
        login_url = reverse("login_user")
        self.dashboard = self.client.post(login_url, self.directorForm, follow=True)
        administrator_list_url = reverse('view_all_administrators')
        self.administrator_list = self.client.post(administrator_list_url, follow=True)

    def test_start_from_administrator_list(self):
        self.assertTemplateUsed(self.administrator_list, 'Dashboards/DashboardParts/AdministratorParts/view_all_administrators.html')

    def test_delete_url(self):
        self.assertEqual(self.url, '/delete_administrator/')

    def test_successful_deletion(self):
        before_count = User.objects.count()
        self.client.post(self.url, {'email': 'janedoe@example.org'}, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count-1)

