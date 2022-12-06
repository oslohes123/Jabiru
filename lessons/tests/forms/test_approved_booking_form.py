"""Tests of the ApprovedBooking form."""
from django.test import TestCase
from django import forms
from lessons.models import User, ApprovedBooking
from lessons.forms import ApprovedBookingForm
import datetime
from lessons.constants import *

class ApprovedBookingFormTestCase(TestCase):
    """Tests of the approved booking form."""

    def setUp(self):

        self.user = User.objects.create_user(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            password='Password456!',
            role = administrator
        )

        self.form_input = {
            'start_date': datetime.date(2023,3,16),
            'day_of_the_week': 'Wednesday',
            'time_of_the_week': datetime.time(16,30,0),
            'total_lessons_count': 14,
            'duration': 75,
            'interval': 3,
            'assigned_teacher': 'Allen Bowman',
            'hourly_rate': 22.50
        }

        self.form_input2 = {
            'start_date': datetime.date(2023,3,16),
            'day_of_the_week': 'Wednesday',
            'time_of_the_week': datetime.time(16,30,0),
            'start_date': datetime.date(2023,3,16),
            'duration': 75,
            'interval': 3,
            'assigned_teacher': 'Allen Bowman',
            'hourly_rate': 9999999
        }

    def test_valid_data_approved_booking_form(self):
        form = ApprovedBookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_contains_required_fields(self):
        form = ApprovedBookingForm()
        self.assertIn('start_date', form.fields)
        self.assertIn('day_of_the_week', form.fields)
        self.assertIn('time_of_the_week', form.fields)
        self.assertIn('total_lessons_count', form.fields)
        self.assertIn('duration', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('assigned_teacher', form.fields)
        self.assertIn('hourly_rate', form.fields)

    def test_invalid_post_form(self):
        form = ApprovedBookingForm(data=self.form_input2)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save(self):
        form = ApprovedBookingForm(data=self.form_input)
        object_num_before_save = ApprovedBooking.objects.count()
        form.save()
        object_num_after_save = ApprovedBooking.objects.count()
        self.assertEqual(object_num_after_save, object_num_before_save + 1)
        
    def test_hourly_rate_cannot_have_more_than_6_digits(self):
        self.form_input['hourly_rate'] = 9999999
        form = ApprovedBookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())