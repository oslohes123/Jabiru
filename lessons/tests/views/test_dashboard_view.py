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
<<<<<<< HEAD
        self.studentUser = User.objects.get(email='dillyparker@example.org')
=======

>>>>>>> refs/remotes/origin/main
        self.studentForm = {
            "email": "dillyparker@example.org",
            "password": "Password123%",
        }
<<<<<<< HEAD
        self.adminUser = User.objects.get(email='janedoe@example.org')
=======
>>>>>>> refs/remotes/origin/main
        self.adminForm = {
            "email": "janedoe@example.org",
            "password": "Password123%"
        }
<<<<<<< HEAD
        self.directorUser = User.objects.get(email='petrapickles@example.org')
=======
>>>>>>> refs/remotes/origin/main
        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }

    def test_student_returned_student_dashboard(self):
        response = self.client.post(self.url,self.studentForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html')

<<<<<<< HEAD
    def test_admin_returned_student_dashboard(self):
        response = self.client.post(self.url,self.adminForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/admin_dashboard.html')

    def test_director_returned_student_dashboard(self):
=======
    def test_admin_returned_admin_dashboard(self):
        response = self.client.post(self.url,self.adminForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/administrator_dashboard.html')

    def test_director_returned_director_dashboard(self):
>>>>>>> refs/remotes/origin/main
        response = self.client.post(self.url,self.directorForm,follow=True)
        self.assertTemplateUsed(response, 'Dashboards/director_dashboard.html')

