"""Tests of the editing an approved lesson"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, ApprovedBooking
from lessons.forms import ApprovedBookingForm
import datetime

class EditLessonViewTestCase(TestCase):
    """Tests of the editing an approved lesson."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = reverse('edit_approved_lessons')
        self.edit_url = reverse('fill_edit_approved_lessons')
        self.request_url = reverse("approve_request")
        login_url = reverse("login_user")
        self.adminUser = User.objects.get(email='janedoe@example.org')
        self.adminForm = {
            "email": "janedoe@example.org",
            "password": "Password123%",
        }
        self.studentUser = User.objects.get(email='dillyparker@example.org')
        
        self.dashboard = self.client.post(login_url, self.adminForm, follow=True)

        self.lesson_approved_form_input = {
            "id": 1,
            'student': self.studentUser,
            "start_date": datetime.date(2023,3,16),
            "day_of_the_week": "Wednesday",
            "time_of_the_week": datetime.time(16,30,0),
            "total_lessons_count": 14,
            "duration": 75,
            "interval": 3,
            "assigned_teacher": "Mr Allen Bowman",
            "hourly_rate": 22.50
        }

        self.lesson_edit_approved_form_input = {
            "id": 1,
            'student': self.studentUser,
            "start_date": datetime.date(2023,3,17),
            "day_of_the_week": "Monday",
            "time_of_the_week": datetime.time(17,30,0),
            "total_lessons_count": 15,
            "duration": 75,
            "interval": 3,
            "assigned_teacher": "Mr Allen Bowman",
            "hourly_rate": 22.50
        }
    
    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/administrator_dashboard.html')

    def test_sign_up_url(self):
        self.assertEqual(self.edit_url, '/fill_edit_approved_lessons/')
    
    def test_make_approved_lesson(self):
        lessons_before = ApprovedBooking.objects.count()
        form = ApprovedBookingForm(data=self.lesson_approved_form_input)
        form.save()
        #self.client.post(self.request_url, self.lesson_approved_form_input, follow=True)
        lessons_after = ApprovedBooking.objects.count()
        self.assertEqual(lessons_before + 1, lessons_after)
    
    def test_get_edit_approve_lesson_page(self):
        self.client.post(self.request_url, self.lesson_approved_form_input, follow=True)
        response = self.client.post(self.edit_url, {'lesson_id': 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/edit_approved.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ApprovedBookingForm))

        