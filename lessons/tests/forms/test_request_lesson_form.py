"""Tests of the LessonRequest form."""
from django.test import TestCase
from django import forms
from lessons.models import User, Lesson
from lessons.forms import RequestForm

class RequestFormTestCase(TestCase):
    """Tests of the request form."""

    def setUp(self):

        self.user = User.objects.create_user(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            password='Password456!'
        )

        self.form_input1 = {
            'availability': '6pm-8pm Sunday',
            'total_lessons_count': 16,
            'duration': 90,
            'interval': 1,
            'further_info': 'prefer to learn guitar'
        }

        self.form_input2 = {
            'availability': '6pm-8pm Sunday',
            'duration': 30,
            'interval': 6,
            'further_info': 'prefer to learn violin'
        }
    
    def test_valid_data_request_form(self):
        form = RequestForm(user=self.user)
        self.assertTrue(form.is_valid())
    
    def test_form_contains_required_fields(self):
        form = RequestForm(user=self.user, data=self.form_input1)
        self.assertIn('availability', form.fields)
        self.assertIn('total_lessons_count', form.fields)
        self.assertIn('duration', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('further_info', form.fields)
    
    def test_valid_post_form(self):
        form = RequestForm(user=self.user, data=self.form_input1)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form = RequestForm(user=self.user, data=self.form_input2)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        form = RequestForm(user=self.user, data=self.form_input1)
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
        form = RequestForm(user=self.user, data=self.form_input2)
        object_num_after_save = Lesson.objects.count()
        form.save()
        object_num_after_save = Lesson.objects.count()
        self.assertEqual(object_num_after_save, object_num_after_save)