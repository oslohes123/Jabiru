"""Tests of the deleting approved lessons view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, ApprovedBooking
from lessons.forms import ApprovedBookingForm
import datetime

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

        self.studentUser = User.objects.get(email='dillyparker@example.org')
        
        #print(self.studentUser)

        self.dashboard = self.client.post(login_url, self.adminForm, follow=True)
        self.lesson_approved_form_input = {
            "id": 1,
            #'student': self.studentUser,
            "start_date": datetime.date(2023,3,16),
            "day_of_the_week": "Wednesday",
            "time_of_the_week": datetime.time(16,30,0),
            "total_lessons_count": 14,
            "duration": 75,
            "interval": 3,
            "assigned_teacher": "Mr Allen Bowman",
            "hourly_rate": 22.50
        }
        self.request_url = reverse("approve_request")
    
    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/administrator_dashboard.html')

    def test_delete_url(self):
        self.assertEqual(self.url, '/delete_approved_lesson/')

    def test_successful_deletion(self):
        # First make a lesson
        form = ApprovedBookingForm(data=self.lesson_approved_form_input)
        form.save()
        before_count = ApprovedBooking.objects.count()
        # Then delete a lesson
        self.client.post(self.url, {'lesson_id': 1}, follow=True)
        after_count = ApprovedBooking.objects.count()
        self.assertEqual(after_count, before_count - 1)