from django.contrib.auth import login
from django.test import TestCase, Client
from django.urls import reverse

from lessons.models import User,Lesson

class MakeRequestTest(TestCase):
    def setUp(self):
        self.url = reverse("make_request")
        self.studentUser = User.objects.create_user(
            'student@example.org',
            first_name='IamaStudent',
            last_name='Doe',
            password="",
            role='student'
        )
        self.studentUser.set_password("Password123")
        self.studentUser.save()
        self.studentLogin = {
            "email":"student@example.org",
            "password":"Password123"
        }
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
        c = Client()
        c.post(reverse("login_user"),self.studentLogin,follow=True)
        originalAmount = Lesson.objects.count()
        c.post(self.url,self.studentLesson,follow=True)
        newAmount = Lesson.objects.count()
        self.assertEqual(originalAmount + 1, newAmount)

