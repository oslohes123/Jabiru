from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from .managers import *
from .constants import *

duration_choices = [(30, "30"), (45, "45"), (60, "60"), (75, "75"), (90, "90"), (105, "105"), (120, "120")]
interval_choices = [(1, "weekly interval"), (2, "fortnightly interval"), (3, "three-weeks interval"),
                    (4, "monthly interval")]

day_of_the_week_choices = [("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"),
                           ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"),
                           ("Sunday", "Sunday")]
role_choices = (
    (student, 'Student'), (adult, 'Adult student or parent'), (administrator, 'Administrator'), (director, 'Director'))


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, max_length=30, blank=False)
    role = models.CharField(max_length=13, choices=role_choices, blank=False)
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               related_name='children', on_delete=models.DO_NOTHING)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_director(self):
        return self.role == director

    @property
    def is_director_or_administrator(self):
        return self.role == director or self.role == administrator

    @property
    def is_student_or_adult(self):
        return self.role == student or self.role == adult

    @property
    def is_adult(self):
        return self.role == adult


class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    availability = models.CharField(max_length=500, blank=False,
                                    help_text='Please specify your available time for taking the lessons.')
    total_lessons_count = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, choices=duration_choices, default=30)
    interval = models.PositiveIntegerField(blank=False, choices=interval_choices, default=1)
    further_info = models.CharField(max_length=500, blank=False,
                                    help_text='Please provide further information such as what you want to learn or '
                                              'your preferred teacher.')
    approve_status = models.BooleanField(default=False)
    objects = CustomLessonManager()


class ApprovedBooking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(blank=False)
    day_of_the_week = models.CharField(blank=False, choices=day_of_the_week_choices, max_length=20)
    time_of_the_week = models.TimeField(blank=False)
    total_lessons_count = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, choices=duration_choices)
    interval = models.PositiveIntegerField(blank=False, choices=interval_choices)
    assigned_teacher = models.CharField(max_length=50, blank=False)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    objects = CustomApprovedBookingManager()

    def total_price(self):
        return self.total_lessons_count * self.hourly_rate * self.duration / 60


class Invoice(models.Model):
    lesson_in_invoice = models.OneToOneField(ApprovedBooking, on_delete=models.CASCADE, blank=False)
    balance_due = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    objects = CustomInvoiceManager()

    def invoice_ref_num(self):
        return f'{self.id}-{self.lesson_in_invoice.student.id}'

class Transaction(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,blank=False)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    objects = CustomTransactionManager()

    def transaction_ref_num(self):
        return f'{self.invoice.id}'
