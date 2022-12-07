from django.test import TestCase
from django import forms
from lessons.forms import TransactionForm
from lessons.models import User

class TransactionFormTestCase(TestCase):
    """Sign up form unit tests"""


    def setUp(self):
        self.form_input = {
            'payment_amount': 10
        }

    def test_form_contains_required_fields(self):
        form = TransactionForm()
        self.assertIn('payment_amount', form.fields)


    def test_payment_amount_cannot_more_than_two_decimals(self):
        self.form_input['payment_amount'] = 0.007
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_payment_amount_cannot_have_more_than_nine_digits(self):
        self.form_input['payment_amount'] = 1000000000
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_payment_amount_cannot_be_negative(self):
        self.form_input['payment_amount'] = -1
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_payment_amount_cannot_be_zero(self):
        self.form_input['payment_amount'] = 0
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())