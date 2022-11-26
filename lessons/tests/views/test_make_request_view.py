from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse

from lessons.models import User,Lesson

class MakeRequestTest(TestCase):
    def setUp(self):
        self.studentUser = User.objects.create_user(
            'student@example.org',
            first_name='IamaStudent',
            last_name='Doe',
            password='Password123',
            role='student'
        )
        self.studentLesson = {
            "student":self.studentUser,
            "availability":"availability",
            "lesson_numbers":2,
            "duration":2,
            "interval":3,
            "further_info":"FurtherInfoBit",
            "approve_status":False
        }

    def test_make_request_input(self):
        self.client.login()
        originalAmount = Lesson.objects.count()
        response = self.client.post(reverse("make_request"),self.studentLesson,follow=True)
        newAmount = Lesson.objects.count()
        self.assertEqual(originalAmount + 1, newAmount)

