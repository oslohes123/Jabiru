"""Tests of the deleting approved lessons view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, ApprovedBooking

class DeleteAdministratorViewTestCase(TestCase):
    """Tests of the deleting approved lessons view."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = 'http://localhost:8000/delete_approved_lesson/1/'
        login_url = reverse("login_user")
        self.adminUser = User.objects.get(email='dillyparker@example.org')
        self.adminForm = {
            "email": "dillyparker@example.org",
            "password": "Password123%",
        }
        self.studentUser = User.objects.get(email='parker@example.org')
        self.studentForm = {
            "email": "parker@example.org",
            "password": "Password123%",
        }