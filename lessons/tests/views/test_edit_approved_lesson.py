"""Tests of the editing an approved lesson"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, ApprovedBooking
from lessons.forms import ApprovedBookingForm
import datetime

class EditLessonViewTestCase(TestCase):
    """Tests of the editing an approved lesson."""

    fixtures = ['lessons/fixtures/user.json', 'lessons/fixtures/lesson.json']

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

        self.lesson_request_form_input = {
            "id": 1,
            "lesson_id": 1,
            "student_id": self.studentUser.id,
            "student": self.studentUser,
            "availability": "I am available on Wednesdays",
            "total_lessons_count": 4,
            "duration": 45,
            "interval": 2,
            "further_info": "Piano lessons",
            "approve_status": False
        }

        self.lesson_approved_form_input = {
            "id": 1,
            "lesson_id": 1,
            "student_id": self.studentUser.id,
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
            "lesson_id": 1,
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
        self.client.post(self.request_url, self.lesson_request_form_input, follow=True)
        form = ApprovedBookingForm(data=self.lesson_approved_form_input)
        form.save()
        response = self.client.post(self.edit_url, {'lesson_id': 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/edit_approved.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ApprovedBookingForm))
    
    def test_edit_approve_lesson(self):
        self.client.post(self.request_url,self.lesson_approved_form_input,follow=True)
        before_count = ApprovedBooking.objects.count()
        response = self.client.post(self.url, self.lesson_edit_approved_form_input, follow=True)
        after_count = ApprovedBooking.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'Dashboards/administrator_dashboard.html')
        changedlesson = ApprovedBooking.objects.get(id=1)
        self.assertEqual(changedlesson.student, self.studentUser)
        self.assertEqual(changedlesson.start_date, datetime.date(2023,3,17))
        self.assertEqual(changedlesson.day_of_the_week, "Monday")
        self.assertEqual(changedlesson.time_of_the_week, datetime.time(17,30,0))
        self.assertEqual(changedlesson.total_lessons_count, 15)
        self.assertEqual(changedlesson.duration, 75)
        self.assertEqual(changedlesson.interval, 3)
        self.assertEqual(changedlesson.assigned_teacher, "Mr Allen Bowman")
        self.assertEqual(changedlesson.hourly_rate, 22.50)
        self.assertTrue(self._is_logged_in())
    
    def test_unsuccessful_approved_edit(self):
        self.lesson_approved_form_input['total_lessons_count'] = 'non_numericals_not_allowed'
        before_count = ApprovedBooking.objects.count()
        response = self.client.post(self.request_url, self.lesson_approved_form_input, follow=True)
        after_count = ApprovedBooking.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/approve_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ApprovedBookingForm))
        self.assertTrue(self._is_logged_in())