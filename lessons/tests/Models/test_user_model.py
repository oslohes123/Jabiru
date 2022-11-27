"""Tests of the user model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import User

# Create your tests here.
class UserModelTestCase(TestCase):
    """Tests of the user model."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(email='dillyparker@example.org')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_email_cannot_be_blank(self): 
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_can_be_30_characters_long(self):
        self.user.email = 'x'*18 + '@example.org'
        self._assert_user_is_valid()

    def test_email_cannot_be_more_than_30_characters_long(self):
        self.user.email = 'x'*19 + '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(email='janedoe@example.org')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_may_contain_numbers(self):
        self.user.email = 'dillyparker21@example.org'
        self._assert_user_is_valid()

    def test_email_must_contain_only_one_at_symbol(self):
        self.user.email = 'dillypark@er@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_least_one_dot(self):
        self.user.email = 'dillyparker@exampleorg'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_after_dot(self):
        self.user.email = 'dillyparker@example.'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_before_dot(self):
        self.user.email = 'dillyparker@.org'
        self._assert_user_is_invalid()


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(email='janedoe@example.org')
        self.user.first_name = 'Dilly'
        self._assert_user_is_valid()

    def test_first_name_may_contain_20_characters(self):
        self.user.first_name = 'x' * 20
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_20_characters(self):
        self.user.first_name = 'x' * 21
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(email='janedoe@example.org')
        self.user.second_name = 'Parker'
        self._assert_user_is_valid()

    def test_last_name_may_contain_20_characters(self):
        self.user.last_name = 'x' * 20
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_20_characters(self):
        self.user.last_name = 'x' * 21
        self._assert_user_is_invalid()


    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()