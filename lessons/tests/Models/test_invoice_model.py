from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.constants import *
from lessons.models import ApprovedBooking, User, Invoice
import datetime

class InvoiceModelTestCase(TestCase):
    """Unit tests for the Invoice model."""

    def setUp(self):
        self.student1 = User.objects.create_user(
            'student1@example.org',
            first_name='John',
            last_name='Smith',
            password="Password456$",
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

        self.invoice1 = Invoice.objects.create_invoice(
            lesson_in_invoice=self.approvedBooking1,
            balance_due=self.approvedBooking1.total_price(),
            payment_paid=550.00
        )

        self.student2 = User.objects.create_user(
            'student2@example.org',
            first_name='Alice',
            last_name='Adams',
            password="Password789%",
            role ="Student"
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

        self.invoice2 = Invoice.objects.create_invoice(
            lesson_in_invoice=self.approvedBooking2,
            balance_due=self.approvedBooking2.total_price(),
            payment_paid=0.00
        )
    
    def test_valid_object(self):
        self._assert_invoice_is_valid()

    
    def test_lesson_in_invoice_cannot_be_blank(self):
        self.invoice1.lesson_in_invoice = None
        self._assert_invoice_is_invalid()
    
    def test_lesson_in_invoice_is_unique(self):
        self.invoice1.lesson_in_invoice = self.invoice2.lesson_in_invoice
        self._assert_invoice_is_invalid()
    
    def test_lesson_in_invoice_request_must_have_been_approved(self):
        self.approvedBooking1.approve_status = False
        self._assert_invoice_is_invalid()
    

    def test_balance_due_cannot_be_blank(self):
        self.invoice1.balance_due = None
        self._assert_invoice_is_invalid()
    
    def test_balance_due_cannot_be_zero(self):
        self.invoice1.balance_due = 0.00
        self._assert_invoice_is_invalid()
    
    def test_balance_due_cannot_be_negative(self):
        self.invoice1.balance_due = -36.50
        self._assert_invoice_is_invalid()

    def test_balance_due_cannot_have_more_than_two_decimals(self):
        self.invoice1.balance_due = 820.234
        self._assert_invoice_is_invalid()

    def test_balance_due_not_unique(self):
        self.invoice1.balance_due = self.invoice2.balance_due
        self._assert_invoice_is_valid()
    

    def test_payment_paid_cannot_be_blank(self):
        self.invoice1.payment_paid = None
        self._assert_invoice_is_invalid()
    
    def test_payment_paid_can_be_zero(self):
        self.invoice1.payment_paid = 0.00
        self._assert_invoice_is_valid()
    
    def test_payment_paid_cannot_be_negative(self):
        self.invoice1.payment_paid = -36.50
        self._assert_invoice_is_invalid()

    def test_payment_paid_cannot_have_more_than_two_decimals(self):
        self.invoice1.payment_paid = 15.234
        self._assert_invoice_is_invalid()

    def test_payment_paid_not_unique(self):
        self.invoice1.payment_paid = self.invoice2.payment_paid
        self._assert_invoice_is_valid()

    def _assert_invoice_is_valid(self):
        try:
            self.invoice1.full_clean()
        except ValidationError:
            self.fail('Test invoice should be valid')

    def _assert_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice1.full_clean()