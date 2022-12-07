from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.constants import *
from lessons.models import Transaction, Invoice, ApprovedBooking, User
import datetime

class InvoiceModelTestCase(TestCase):
    """Unit tests for the transaction model."""

    def setUp(self):
        self.student = User.objects.create_user(
            'student1@example.org',
            first_name='John',
            last_name='Smith',
            password="Password456$",
            role ="Student"
        )

        self.approvedBooking = ApprovedBooking.objects.create_approvedBooking(
            student=self.student,
            start_date=datetime.date(2023, 3, 5),
            day_of_the_week="Friday",
            time_of_the_week=datetime.time(20, 0, 0),
            total_lessons_count=5,
            duration=90,
            interval=2,
            assigned_teacher='Paul Anderson',
            hourly_rate=30.00
        )

        self.invoice = Invoice.objects.create_invoice(
            lesson_in_invoice=self.approvedBooking,
            balance_due=self.approvedBooking.total_price()
        )

        self.transaction = Transaction.objects.create_transaction(
            invoice=self.invoice,
            payment_amount=self.approvedBooking.total_price()
        )


    def test_valid_object(self):
        self._assert_transaction_is_valid()

    def test_invoice_in_transaction_cannot_be_blank(self):
        self.transaction.invoice = None
        self._assert_transaction_is_invalid()

    def test_payment_amount_in_transaction_cannot_be_blank(self):
        self.transaction.payment_amount = None
        self._assert_transaction_is_invalid()

    def test_payment_amount_in_transaction_cannot_be_zero(self):
        self.transaction.payment_amount = 0
        self._assert_transaction_is_invalid()

    def test_payment_amount_in_transaction_cannot_be_negative(self):
        self.transaction.payment_amount = -1
        self._assert_transaction_is_invalid()

    def test_payment_amount_in_transaction_cannot_have_more_than_two_decimals(self):
        self.transaction.payment_amount = 100.232
        self._assert_transaction_is_invalid()

    def test_payment_amount_in_transaction_cannot_have_more_than_eight_digits(self):
        self.transaction.payment_amount = 100000000
        self._assert_transaction_is_invalid()

    
    def _assert_transaction_is_valid(self):
        try:
            self.transaction.full_clean()
        except ValidationError:
            self.fail('Test transaction should be valid')

    def _assert_transaction_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transaction.full_clean()