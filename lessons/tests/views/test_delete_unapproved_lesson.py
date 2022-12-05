"""Tests of the deleting unapproved lessons view."""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Lesson

class DeleteAdministratorViewTestCase(TestCase):
    """Tests of the deleting unapproved lessons view."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.url = 'http://localhost:8000/delete_lesson/1/'
        login_url = reverse("login_user")
        self.studentUser = User.objects.get(email='dillyparker@example.org')
        self.studentForm = {
            "email": "dillyparker@example.org",
            "password": "Password123%",
        }
        self.dashboard = self.client.post(login_url, self.studentForm, follow=True)
        self.lesson_request_form_input = {
            "id": 1,
            "student": self.studentUser,
            "availability": "I am available on Wednesdays",
            "total_lessons_count": 4,
            "duration": 45,
            "interval": 2,
            "further_info": "Piano lessons",
            "approve_status": False
        }
        self.request_url = reverse("make_request")

    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/student_dashboard.html')

    def test_delete_url(self):
        self.assertEqual(self.url,'http://localhost:8000/delete_lesson/1/')

    def test_successful_deletion(self):
        # First make a lesson
        self.client.post(self.request_url,self.lesson_request_form_input,follow=True)
        before_count = Lesson.objects.count()
        # Then delete a lesson
        self.client.post(self.url, follow=True)
        after_count = Lesson.objects.count()
        self.assertEqual(after_count, before_count-1)