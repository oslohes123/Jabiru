"""Tests of the ApprovedBooking model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import User, ApprovedBooking
import datetime

# Create your tests here.
class ApprovedBookingModelTestCase(TestCase):
    """Tests of the ApporvedBooking model."""

    def setUp(self):
        self.student1 = User.objects.create_user(
            'student1@example.org',
            first_name='John',
            last_name='Smith',
            password="Password456$",
            role ='student'
        )

        self.student2 = User.objects.create_user(
            'student2@example.org',
            first_name='Alice',
            last_name='Adams',
            password="Password789%",
            role ='student'
        )

        self.lessonRequest1 = ApprovedBooking.objects.create_approvedBooking(
            student=self.student1,
            start_date=datetime.date(2023, 1, 13),
            day_of_the_week = day_of_the_week,
            lesson_numbers=5,
            duration=90,
            interval=2,
            teacher='Anderson',
            hourly_rate=30.00,
            approve_status=True,
        )

        self.lessonRequest2 = ApprovedBooking.objects.create_approvedBooking(
            student=self.student2,
            availability="7pm-9pm Monday",
            lesson_numbers=4,
            duration=120,
            interval = 4,
            further_info = "I want to learn violin and be taught by Mr Anderson",
            approve_status = False,
        )

    
    def _assert_approved_booking_is_valid(self):
        try:
            self.lessonRequest1.full_clean()
        except ValidationError:
            self.fail('Test lesson request should be valid')

    def _assert_approved_booking_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lessonRequest1.full_clean()