from django.test import TestCase
from django.urls import reverse
from lessons.constants import *
from lessons.models import User,Lesson

class DashbaordCase(TestCase):
    def setUp(self):
        #self.url = reverse("login_user")
        self.studentUser = User.objects.create_user(
            'student@example.org',
            first_name='IamaStudent',
            last_name='Doe',
            password='Password123',
            role=student
        )
        self.studentForm = {
            "email":"student@example.org",
            "password":"Password123",
        }
        self.adminUser = User.objects.create_user(
            'admin@example.org',
            first_name='Iamaadmin',
            last_name='Doe',
            password='Password123',
            role=administrator
        )
        self.adminForm = {
            "email": "admin@example.org",
            "password": "Password123",
        }

        self.lesson = Lesson.objects.create_lesson(
            student = User.objects.get(email = 'student@example.org'),
            availability = 'From 11:00 to 13:00',
            lesson_numbers = 3,
            duration = 100,
            interval = 2,
            further_info = 'Banjo lessons with Mr.Banjo',
            approve_status = True
        )
        
