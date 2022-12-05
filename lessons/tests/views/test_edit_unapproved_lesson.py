"""Tests of the editing an unapproved lesson"""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User, Lesson

class EditLessonViewTestCase(TestCase):
    """Tests of the editing an unapproved lesson."""

    fixtures = ['lessons/fixtures/user.json',]

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def setUp(self):
        self.totalLessons = Lesson.objects.count()
        self.edit_url = 'http://localhost:8000/edit_unapproved_lessons/1/'
        self.request_url = reverse("make_request")
        login_url = reverse("login_user")
        self.studentUser = User.objects.get(email='dillyparker@example.org')
        self.studentForm = {
            "email": "dillyparker@example.org",
            "password": "Password123%",
        }
        self.dashboard = self.client.post(login_url,self.studentForm,follow=True)
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
        self.lesson_edit_form_input = {
            "id": 1,
            "student": self.studentUser,
            "availability": "I am available on Tuesdays",
            "total_lessons_count": 2,
            "duration": 30,
            "interval": 1,
            "further_info": "I will need extra help!",
            "approve_status": False
        }

    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/student_dashboard.html')

    def test_sign_up_url(self):
        self.assertEqual(self.edit_url,'http://localhost:8000/edit_unapproved_lessons/1/')

    def test_make_lesson_request(self):
        lessons_before = Lesson.objects.count()
        self.client.post(self.request_url,self.lesson_request_form_input,follow=True)
        lessons_after = Lesson.objects.count()
        self.assertEqual(lessons_before + 1, lessons_after)

    def test_get_edit_page(self):
        self.client.post(self.request_url,self.lesson_request_form_input,follow=True)
        response = self.client.post(self.edit_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/make_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))

    def test_edit_lesson(self):
        self.client.post(self.request_url,self.lesson_request_form_input,follow=True)
        before_count = User.objects.count()
        response = self.client.post(self.edit_url, self.lesson_edit_form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/make_request.html')
        changedlesson = Lesson.objects.get(id=1)
        self.assertEqual(changedlesson.availability, "I am available on Tuesdays",)
        self.assertEqual(changedlesson.total_lessons_count, 2)
        self.assertEqual(changedlesson.duration, 30)
        self.assertEqual(changedlesson.interval, 1)
        self.assertEqual(changedlesson.further_info, "I will need extra help!")
        self.assertTrue(self._is_logged_in())

    def test_unsuccessful_lesson_edit(self):
        self.lesson_request_form_input['total_lessons_count'] = 'non_numericals_not_allowed'
        before_count = User.objects.count()
        response = self.client.post(self.request_url,self.lesson_request_form_input,follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/make_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertTrue(self._is_logged_in())