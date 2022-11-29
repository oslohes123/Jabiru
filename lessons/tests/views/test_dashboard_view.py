from django.test import TestCase
from django.urls import reverse

from lessons.models import User


class DashboardCase(TestCase):
    """Tests of the dashboard view"""
    fixtures = [
        'lessons/fixtures/user.json',
        ]
    def setUp(self):
        self.url = reverse("login_user")
        self.studentForm = {
            "email": "dillyparker@example.org",
            "password": "Password123%",
        }

        self.adminForm = {
            "email": "janedoe@example.org",
            "password": "Password123%"
        }

        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }
    # Test commit
    def test_student_returned_student_dashboard(self):
        response = self.client.post(self.url,self.studentForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html')

    def test_admin_returned_student_dashboard(self):
        response = self.client.post(self.url,self.adminForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/administrator_dashboard.html')

    def test_director_returned_student_dashboard(self):
        response = self.client.post(self.url,self.directorForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/director_dashboard.html')

