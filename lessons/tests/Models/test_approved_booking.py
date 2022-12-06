"""Tests of the ApprovedBooking model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.constants import *
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
            role ="Student"
        )

        self.student2 = User.objects.create_user(
            'student2@example.org',
            first_name='Alice',
            last_name='Adams',
            password="Password789%",
            role ="Student"
        )

        self.approvedBooking1 = ApprovedBooking.objects.create_approvedBooking(
            student=self.student1,
            start_date=datetime.date(2023, 3, 5),
            day_of_the_week="Friday",
            time_of_the_week=datetime.time(20, 0, 0),
            total_lesson_count=5,
            duration=90,
            interval=2,
            assigned_teacher='Paul Anderson',
            hourly_rate=30.00,
            approve_status=True
        )

        self.approvedBooking2 = ApprovedBooking.objects.create_approvedBooking(
            student=self.student2,
            start_date=datetime.date(2023, 3, 5),
            day_of_the_week="Monday",
            time_of_the_week=datetime.time(20, 0, 0),
            total_lesson_count=4,
            duration=120,
            interval = 4,
            assigned_teacher="Joe Miller",
            hourly_rate=25.50,
            approve_status = True
        )

    
    def test_valid_approved_booking(self):
        self._assert_approved_booking_is_valid()

    
    def test_student_cannot_be_blank(self):
        self.approvedBooking1.student = None
        self._assert_approved_booking_is_invalid()

    def test_student_not_unique(self):
        self.approvedBooking1.student = self.approvedBooking2.student
        self._assert_approved_booking_is_valid()


    def test_start_date_cannot_be_blank(self):
        self.approvedBooking1.start_date = None
        self._assert_approved_booking_is_invalid()

    def test_start_date_not_unique(self):
        self.approvedBooking1.start_date = self.approvedBooking2.start_date
        self._assert_approved_booking_is_valid()


    def test_day_of_the_week_cannot_be_blank(self):
        self.approvedBooking1.day_of_the_week = None
        self._assert_approved_booking_is_invalid()

    def test_day_of_the_week_not_unique(self):
        self.approvedBooking1.day_of_the_week = self.approvedBooking2.day_of_the_week
        self._assert_approved_booking_is_valid()


    def test_time_of_the_week_cannot_be_blank(self):
        self.approvedBooking1.time_of_the_week = None
        self._assert_approved_booking_is_invalid()

    def test_time_of_the_week_not_unique(self):
        self.approvedBooking1.time_of_the_week = self.approvedBooking2.time_of_the_week
        self._assert_approved_booking_is_valid()


    def test_total_lesson_count_cannot_be_blank(self):
        self.approvedBooking1.total_lesson_count = None
        self._assert_approved_booking_is_invalid()

    def test_total_lesson_count_not_unique(self):
        self.approvedBooking1.total_lesson_count = self.approvedBooking2.total_lesson_count
        self._assert_approved_booking_is_valid()

    def test_total_lesson_count_cannot_be_negative(self):
        self.approvedBooking1.total_lesson_count = -10
        self._assert_approved_booking_is_invalid()
    
    def test_total_lesson_count_cannot_be_zero(self):
        self.approvedBooking1.total_lesson_count = 0
        self._assert_approved_booking_is_invalid()


    def test_duration_cannot_be_blank(self):
        self.approvedBooking1.duration = None
        self._assert_approved_booking_is_invalid()

    def test_duration_not_unique(self):
        self.approvedBooking1.duration = self.approvedBooking2.duration
        self._assert_approved_booking_is_valid()

    def test_duration_cannot_be_negative(self):
        self.approvedBooking1.duration = -3
        self._assert_approved_booking_is_invalid()
    
    def test_duration_cannot_be_zero(self):
        self.approvedBooking1.duration = 0
        self._assert_approved_booking_is_invalid()

    def test_duration_can_equal_to_120(self):
        self.approvedBooking1.duration = 120
        self._assert_approved_booking_is_valid()


    def test_interval_cannot_be_blank(self):
        self.approvedBooking1.interval = None
        self._assert_approved_booking_is_invalid()

    def test_interval_not_unique(self):
        self.approvedBooking1.interval = self.approvedBooking2.interval
        self._assert_approved_booking_is_valid()

    def test_interval_cannot_be_negative(self):
        self.approvedBooking1.interval = -4
        self._assert_approved_booking_is_invalid()
    
    def test_interval_cannot_be_zero(self):
        self.approvedBooking1.interval = 0
        self._assert_approved_booking_is_invalid()

    def test_interval_can_equal_to_8(self):
        self.approvedBooking1.interval = 8
        self._assert_approved_booking_is_valid()


    def test_assigned_teacher_can_not_be_blank(self):
        self.approvedBooking1.assigned_teacher = ''
        self._assert_approved_booking_is_invalid()

    def test_assigned_teacher_not_unique(self):
        self.approvedBooking1.assigned_teacher = self.approvedBooking2.assigned_teacher
        self._assert_approved_booking_is_valid()

    def test_assigned_teacher_may_contain_50_characters(self):
        self.approvedBooking1.assigned_teacher = 'a' * 50
        self._assert_approved_booking_is_valid()

    def test_assigned_teacher_must_not_contain_more_than_50_characters(self):
        self.approvedBooking1.assigned_teacher = 'a' * 51
        self._assert_approved_booking_is_invalid()


    def test_hourly_rate_cannot_be_blank(self):
        self.approvedBooking1.hourly_rate = None
        self._assert_approved_booking_is_invalid()

    def test_hourly_rate_not_unique(self):
        self.approvedBooking1.hourly_rate = self.approvedBooking2.hourly_rate
        self._assert_approved_booking_is_valid()

    def test_hourly_rate_cannot_be_negative(self):
        self.approvedBooking1.hourly_rate = -10.00
        self._assert_approved_booking_is_invalid()
    
    def test_hourly_rate_cannot_be_zero(self):
        self.approvedBooking1.hourly_rate = 0.00
        self._assert_approved_booking_is_invalid()
    
    def test_hourly_rate_cannot_have_more_than_two_decimals(self):
        self.approvedBooking1.hourly_rate = 15.123
        self._assert_approved_booking_is_invalid()


    def _assert_approved_booking_is_valid(self):
        try:
            self.approvedBooking1.full_clean()
        except ValidationError:
            self.fail('Test approved booking should be valid')

    def _assert_approved_booking_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.approvedBooking1.full_clean()
