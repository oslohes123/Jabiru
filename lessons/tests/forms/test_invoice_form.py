"""Tests of the Invoice form."""
from django.test import TestCase
from django import forms
from lessons.models import User, ApprovedBooking, Invoice
from lessons.forms import InvoiceForm
import datetime

class RequestFormTestCase(TestCase):
    """Tests of the invoice form."""
    def setUp(self):

        self.user = User.objects.create_user(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            password='Password456!'
        )

        self.approvedBooking = ApprovedBooking.objects.create_approvedBooking(
            user=self.user,
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

        self.form_input1 = {
            'balance_due': 1200.00,
            'payment_paid': 200.00
        }

        self.form_input2 = {
            'balance_due': 1200.00
        }

    def test_valid_data_invoice_form(self):
        form = InvoiceForm(user=self.approvedBooking)
        self.assertTrue(form.is_valid())

    def test_form_contains_required_fields(self):
        form = InvoiceForm()
        self.assertIn('balance_due', form.fields)
        self.assertIn('payment_paid', form.fields)

    def test_valid_post_form(self):
        form = InvoiceForm(user=self.user, data=self.form_input1)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form = InvoiceForm(user=self.user, data=self.form_input2)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = InvoiceForm(user=self.user, data=self.form_input1)
        object_num_before_save = Invoice.objects.count()
        form.save()
        object_num_after_save = Invoice.objects.count()
        self.assertEqual(object_num_after_save, object_num_before_save + 1)
        request_of_lesson = Invoice.objects.get(student=self.user)
        self.assertEqual(request_of_lesson.balance_due, 1200.00)
        self.assertEqual(request_of_lesson.payment_paid, 200.00)

    def test_invalid_form_does_not_save(self):
        form = InvoiceForm(user=self.user, data=self.form_input2)
        object_num_after_save = Invoice.objects.count()
        form.save()
        object_num_after_save = Invoice.objects.count()
        self.assertEqual(object_num_after_save, object_num_after_save)
    