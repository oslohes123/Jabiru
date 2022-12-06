from django.test import TestCase
from django.urls import reverse

from lessons.models import User


class DashboardCase(TestCase):
    """Tests of the administrator list view"""

    fixtures = ['lessons/fixtures/user.json']

    def setUp(self):
        self.url = reverse('view_all_administrators')
        self.directorUser = User.objects.get(email='petrapickles@example.org')
        self.directorForm = {
            "email": "petrapickles@example.org",
            "password": "Password123%",
        }
        self.adminUser = User.objects.get(email='janedoe@example.org')
        self.adminForm = {
            "email": "janedoe@example.org",
            "password": "Password123%"
        }
        login_url = reverse("login_user")
        self.dashboard = self.client.post(login_url,self.directorForm,follow=True)
        #self.client.post(login_url,self.adminUser)
        self.form_input = {
            'first_name': 'Name',
            'last_name': 'Lastname',
            'email': 'namelastname@example.org',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def test_start_from_dashboard(self):
        self.assertTemplateUsed(self.dashboard, 'Dashboards/director_dashboard.html')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/view_all_administrators/')

    def invalid_admins_not_appearing(self):
        self.form_input['email'] = 'bademail'
        before_count = User.objects.count()
        response = self.client.post(self.login_url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)

    def test_admin_is_added_to_view(self):
        self._create_test_users(5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboards/DashboardParts/AdministratorParts/view_all_administrators.html')
        #self.assertEqual(len(response.context['users']), 15)
        for user_id in range(5):
            self.assertContains(response, f'user{user_id}@test.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')

    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            User.objects.create_user(f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                role='Administrator',
            )
    