"""Tests of the LessonRequest form."""
from django.test import TestCase
from django import forms
from lessons.models import User, Lesson
from lessons.forms import RequestForm
from lessons.constants import student

class RequestFormTestCase(TestCase):
    """Tests of the request form."""

    def setUp(self):

        self.user = User.objects.create_user(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            password='Password456!',
            role = student
        )

        self.valid_input = {
            'availability': '6pm-8pm Sunday',
            'total_lessons_count': 16,
            'duration': 90,
            'interval': 1,
            'further_info': 'prefer to learn guitar'
        }

        self.invalid_input = {
            'availability': '6pm-8pm Sunday',
            'duration': 30,
            'interval': 6,
            'further_info': 'prefer to learn violin'
        }
    
    def test_valid_data_request_form(self):
        form = RequestForm(data =self.valid_input)
        self.assertTrue(form.is_valid())
    
    def test_form_contains_required_fields(self):
        form = RequestForm(data=self.valid_input)
        self.assertIn('availability', form.fields)
        self.assertIn('total_lessons_count', form.fields)
        self.assertIn('duration', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('further_info', form.fields)
    
    def test_valid_post_form(self):
        form = RequestForm(data=self.valid_input)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form = RequestForm(data = self.invalid_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        form = RequestForm(data=self.valid_input)
        object_num_before_save = Lesson.objects.count()
        form.save()
        object_num_after_save = Lesson.objects.count()
        self.assertEqual(object_num_after_save, object_num_before_save + 1)
        request_of_lesson = Lesson.objects.get(student=self.user)
        self.assertEqual(request_of_lesson.availability, '6pm-8pm Sunday')
        self.assertEqual(request_of_lesson.total_lessons_count, 16)
        self.assertEqual(request_of_lesson.duration, 90)
        self.assertEqual(request_of_lesson.interval, 1)
        self.assertEqual(request_of_lesson.further_info, 'prefer to learn guitar')
    
    def test_invalid_form_does_not_save(self):
        form = RequestForm(data=self.invalid_input)
        self.assertFalse(form.is_valid())