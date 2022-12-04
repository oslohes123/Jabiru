from django.contrib.auth import login
from django.test import TestCase, Client
from django.urls import reverse
from lessons.constants import *
from lessons.models import User,Lesson
from django.forms.models import model_to_dict


class MakeRequestTest(TestCase):
    def setUp(self):
        self.url = reverse("make_request")
        self.studentUser = User.objects.create_user(
            'student@example.org',
            first_name='IamaStudent',
            last_name='Doe',
            password="",
            role = student
        )
        # set_password ensures a hash of the password is stored and not the plain-text password
        self.studentUser.set_password("Password123")
        self.studentUser.save()
        self.studentLogin = {
            "email":"student@example.org",
            "password":"Password123"
        }
        self.studentLesson = {
            "id": 1,
            "student": self.studentUser,
            "availability": "I am available on Tuesdays",
            "total_lessons_count": 2,
            "duration": 30,
            "interval": 1,
            "further_info": "I will need extra help!",
            "approve_status": False
        }
        self.c = Client()
        self.c.post(reverse("login_user"), self.studentLogin, follow=True)
        
    def test_make_request_input(self):
        original_amount = Lesson.objects.count()
        self.c.post(self.url,self.studentLesson,follow=True)
        new_amount = Lesson.objects.count()
        self.assertEqual(original_amount + 1, new_amount)

    def test_values_for_test_are_correct(self):
        self.c.post(self.url,self.studentLesson,follow=True)
        inserted_lesson = model_to_dict(Lesson.objects.get(student = self.studentUser))
        # Lessons.objects.get() returns the pk for the student.
        self.studentLesson['student'] = self.studentLesson['student'].pk
        self.assertDictEqual(inserted_lesson,self.studentLesson)

