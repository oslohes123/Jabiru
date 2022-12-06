"""Tests for deleting approved lessons by the admin"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, ApprovedBooking

class DeleteAdministratorViewTestCase(TestCase):
    """Tests of the deleting unapproved lessons view."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.totalApprovedLessons = ApprovedBooking.objects.count()
        self.edit_url = 'http://localhost:8000/edit_approved_lessons/1/'
        self.request_url = reverse("make_request")
        login_url = reverse("login_user")
        self.studentUser = User.objects.get(email='dillyparker@example.org')
        self.studentForm = {
            "email": "dillyparker@example.org",
            "password": "Password123%",
        }