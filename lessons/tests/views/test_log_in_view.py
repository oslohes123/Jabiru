"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm
from lessons.models import User

class LogInViewTestCase(TestCase):
    """Tests of the log in view."""
    
    fixtures = ['lessons/fixtures/user.json']

    def setUp(self):
        self.url = reverse('login_user')
        self.user = User.objects.get(email='dillyparker@example.org')

    def reverse_with_next(self, url_name, next_url):
        url = reverse(url_name)
        url += f"?next={next_url}"
        return url

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def test_log_in_url(self):
        self.assertEqual(self.url,'/login/')

    """ def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0) """

    """ def test_get_log_in_with_redirect(self):
        destination_url = reverse('dashboard')
        self.url = self.reverse_with_next('login_user', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0) """

    """ def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123%")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html') """

    def test_unsuccesful_log_in(self):
        form_input = { 'email': 'dillyparker@example.org@example.org', 'password': 'WrongPassword123%' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_username(self):
        form_input = { 'email': '', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        form_input = { 'email': 'dillyparker@example.org@example.org', 'password': '' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_succesful_log_in(self):
        form_input = { 'email': 'dillyparker@example.org', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0) #works

    def test_succesful_log_in_with_redirect(self):
        redirect_url = reverse('dashboard')
        form_input = { 'email': 'dillyparker@example.org', 'password': 'Password123%', 'next': redirect_url }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """ def test_post_log_in_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123%")
        form_input = { 'email': 'wronguser@email.org', 'password': 'WrongPassword123%' }
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'Dashboards/student_dashboard.html') """

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = { 'email': 'dillyparker@example.org', 'password': 'Password123%' }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    """ def test_post_log_in_with_incorrect_credentials_and_redirect(self):
        redirect_url = reverse('dashboard')
        form_input = { 'email': 'dillyparker@example.org', 'password': 'WrongPassword123%', 'next':redirect_url }
        response = self.client.post(self.url, form_input)
        next = response.context['next']
        self.assertEqual(next, redirect_url) """