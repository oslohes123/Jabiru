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
        self.url = reverse('delete_approved_lesson')
        login_url = reverse("login_user")
        self.adminUser = User.objects.get(email='janedoe@example.org')
        self.adminForm = {
            "email": "janedoe@example.org",
            "password": "Password123%",
        }
        print(self.adminUser)

        self.studentUser = User.objects.get(email='dillyparker@example.org')
        
        #print(self.studentUser)

        self.dashboard = self.client.post(login_url, self.adminForm, follow=True)
        self.lesson_approved_form_input = {
            "id": 1,
            "student": self.studentUser,
            "start_date": "2022-12-06",
            "day_of_the_week": "Monday" ,
            "time_of_the_week": "13:00" ,
            "total_lessons_count": 4,
            "duration": 45,
            "interval": 2,
            "assigned_teacher": "Mr White",
            "hourly_rate": 30.00
        }
        self.request_url = reverse("approve_request")

    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/administrator_dashboard.html')

    def test_delete_url(self):
        self.assertEqual(self.url, '/delete_approved_lesson/')

    def test_successful_deletion(self):
        # First make a lesson
        self.client.post(self.request_url, self.lesson_approved_form_input, follow=True)
        before_count = ApprovedBooking.objects.count()
        # Then delete a lesson
        self.client.post(self.url, {'lesson_id': 1}, follow=True)
        after_count = ApprovedBooking.objects.count()
        self.assertEqual(after_count, before_count - 1)