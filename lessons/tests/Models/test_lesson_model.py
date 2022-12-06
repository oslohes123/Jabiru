"""Tests of the Lesson model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.constants import *
from lessons.models import User, Lesson

# Create your tests here.
class LessonModelTestCase(TestCase):
    """Tests of the Lesson model."""

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

        self.lessonRequest1 = Lesson.objects.create_lesson(
            student=self.student1,
            availability="6pm-7pm Friday, 10am-11am Saturday",
            total_lessons_count=8,
            duration=45,
            interval = 2,
            further_info = "I want to learn piano",
            approve_status = False,
        )

        self.lessonRequest2 = Lesson.objects.create_lesson(
            student=self.student2,
            availability="7pm-9pm Monday",
            total_lessons_count=4,
            duration=120,
            interval = 4,
            further_info = "I want to learn violin and be taught by Mr Anderson",
            approve_status = False,
        )


    def test_valid_lesson_request(self):
        self._assert_lesson_request_is_valid()

    
    def test_student_cannot_be_blank(self):
        self.lessonRequest1.student = None
        self._assert_lesson_request_is_invalid()

    def test_student_not_unique(self):
        self.lessonRequest1.student = self.lessonRequest2.student
        self._assert_lesson_request_is_valid()


    def test_availability_can_not_be_blank(self):
        self.lessonRequest1.availability = ''
        self._assert_lesson_request_is_invalid()

    def test_availability_not_unique(self):
        self.lessonRequest1.availability = self.lessonRequest2.availability
        self._assert_lesson_request_is_valid()

    def test_availability_may_contain_500_characters(self):
        self.lessonRequest1.availability = 'a' * 500
        self._assert_lesson_request_is_valid()

    def test_availability_must_not_contain_more_than_500_characters(self):
        self.lessonRequest1.availability = 'a' * 501
        self._assert_lesson_request_is_invalid()


    def test_total_lessons_count_cannot_be_blank(self):
        self.lessonRequest1.total_lessons_count = None
        self._assert_lesson_request_is_invalid()

    def test_total_lessons_count_not_unique(self):
        self.lessonRequest1.total_lessons_count = self.lessonRequest2.total_lessons_count
        self._assert_lesson_request_is_valid()

    def test_total_lessons_count_cannot_be_negative(self):
        self.lessonRequest1.total_lessons_count = -10
        self._assert_lesson_request_is_invalid()
    
    def test_total_lessons_count_cannot_be_zero(self):
        self.lessonRequest1.total_lessons_count = 0
        self._assert_lesson_request_is_invalid()


    def test_duration_cannot_be_blank(self):
        self.lessonRequest1.duration = None
        self._assert_lesson_request_is_invalid()

    def test_duration_not_unique(self):
        self.lessonRequest1.duration = self.lessonRequest2.duration
        self._assert_lesson_request_is_valid()

    def test_duration_cannot_be_negative(self):
        self.lessonRequest1.duration = -3
        self._assert_lesson_request_is_invalid()
    
    def test_duration_cannot_be_zero(self):
        self.lessonRequest1.duration = 0
        self._assert_lesson_request_is_invalid()
    
    def test_duration_can_equal_to_120(self):
        self.lessonRequest1.duration = 120
        self._assert_lesson_request_is_valid()

    
    def test_interval_cannot_be_blank(self):
        self.lessonRequest1.interval = None
        self._assert_lesson_request_is_invalid()

    def test_interval_not_unique(self):
        self.lessonRequest1.interval = self.lessonRequest2.interval
        self._assert_lesson_request_is_valid()

    def test_interval_cannot_be_negative(self):
        self.lessonRequest1.interval = -4
        self._assert_lesson_request_is_invalid()
    
    def test_interval_cannot_be_zero(self):
        self.lessonRequest1.interval = 0
        self._assert_lesson_request_is_invalid()

    def test_interval_can_equal_to_8(self):
        self.lessonRequest1.duration = 8
        self._assert_lesson_request_is_valid()

    
    def test_further_info_can_not_be_blank(self):
        self.lessonRequest1.further_info = ''
        self._assert_lesson_request_is_invalid()

    def test_further_info_not_unique(self):
        self.lessonRequest1.further_info = self.lessonRequest2.further_info
        self._assert_lesson_request_is_valid()

    def test_further_info_may_contain_500_characters(self):
        self.lessonRequest1.further_info = 'a' * 500
        self._assert_lesson_request_is_valid()

    def test_further_info_must_not_contain_more_than_500_characters(self):
        self.lessonRequest1.further_info = 'a' * 501
        self._assert_lesson_request_is_invalid()


    def _assert_lesson_request_is_valid(self):
        try:
            self.lessonRequest1.full_clean()
        except ValidationError:
            self.fail('Test lesson request should be valid')

    def _assert_lesson_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lessonRequest1.full_clean()