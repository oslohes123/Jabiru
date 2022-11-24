from django.test import TestCase
from django.urls import reverse

from lessons.models import User


class DashbaordCase(TestCase):
    def setUp(self):
        self.url = reverse("login_user")
        self.studentUser = User.objects.create_user(
            'student@example.org',
            first_name='IamaStudent',
            last_name='Doe',
            password='Password123',
            role='student'
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
            role='admin'
        )
        self.adminForm = {
            "email": "admin@example.org",
            "password": "Password123",
        }
        self.directorUser = User.objects.create_user(
            'director@example.org',
            first_name='Iamadirector',
            last_name='Doe',
            password='Password123',
            role='director'
        )
        self.directorForm = {
            "email": "director@example.org",
            "password": "Password123",
        }

    def test_student_returned_student_dashboard(self):
        response = self.client.post(self.url,self.studentForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html')

    def test_admin_returned_student_dashboard(self):
        response = self.client.post(self.url,self.adminForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/admin_dashboard.html')

    def test_director_returned_student_dashboard(self):
        response = self.client.post(self.url,self.directorForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/director_dashboard.html')

