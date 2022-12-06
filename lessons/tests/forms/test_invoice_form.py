"""Tests of the Invoice form."""
from django.test import TestCase
from django import forms
from lessons.models import User, ApprovedBooking, Invoice
from lessons.forms import InvoiceForm
import datetime

class InvoiceFormTestCase(TestCase):
    """Tests of the invoice form."""
    def setUp(self):

        self.user = User.objects.create_user(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            role='Student',
            password='Password456!'
        )
        
        self.approvedBooking = ApprovedBooking.objects.create_approvedBooking(
            student=self.user,
            start_date=datetime.date(2023, 3, 5),
            day_of_the_week="Friday",
            time_of_the_week=datetime.time(20, 0, 0),
            total_lessons_count=5,
            duration=90,
            interval=2,
            assigned_teacher='Paul Anderson',
            hourly_rate=30.00
        )

        self.form_input = {
            'lesson_in_invoice': self.approvedBooking,
            'balance_due': 1200.00,
        }

    def test_form_contains_required_fields(self):
        form = InvoiceForm()
        self.assertIn('balance_due', form.fields)
        self.assertIn('lesson_in_invoice', form.fields)

    def test_valid_post_form(self):
        form = InvoiceForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_balance_cannot_have_more_than_8_digits(self):
        self.form_input['balance_due'] = 100000000
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_balance_cannot_have_more_than_2_decimals(self):
        self.form_input['balance_due'] = 1200.001
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())