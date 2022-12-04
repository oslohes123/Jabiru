from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
from .managers import CustomUserManager, CustomLessonManager, CustomApprovedBookingManager
from .constants import *

duration_choices = [(30, "30"), (45, "45"), (60, "60")]
interval_choices = [(1, "1"), (2, "2")]

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, max_length=30, blank=False)
    role = models.CharField(default='Student', max_length=10)

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
    def is_student(self):
        return self.role == student

class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    availability = models.CharField(max_length=500, blank=False,
                                    help_text='Please specify your available time for taking the lessons.')
    total_lessons_count = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, choices=duration_choices, default=30)
    interval = models.PositiveIntegerField(blank=False, choices=interval_choices, default=1)
    further_info = models.CharField(max_length=500, blank=False,
                                    help_text='Please provide further information such as what you want to learn or your preferred teacher.')
    approve_status = models.BooleanField(default=False)
    objects = CustomLessonManager()


class ApprovedBooking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(blank=False)
    day_of_the_week = models.DateTimeField(blank=False)
    total_lessons_count = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, choices=duration_choices)
    interval = models.PositiveIntegerField(blank=False, choices=interval_choices)
    teacher = models.CharField(max_length=50, blank=False)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    objects = CustomApprovedBookingManager()

    def total_price(self):
        return self.total_lessons_count * self.hourly_rate * self.duration/60


class Invoice(models.Model):
    lesson_in_invoice = models.OneToOneField(ApprovedBooking, on_delete=models.CASCADE,blank=False)
    balance_due = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_paid = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def invoice_ref_num(self):
        return f'{self.lesson_in_invoice.student.id}-{self.id}'
