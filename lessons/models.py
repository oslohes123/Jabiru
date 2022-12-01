from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator
from decimal import Decimal
from .managers import CustomUserManager,CustomLessonManager, CustomApprovedBookingManager

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

class Lesson(models.Model):

    duration_choices = [(1,"30"),(2,"45"),(3,"60")]
    interval_choices = [(1,"1"),(2,"2")]

    student = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    availability = models.CharField(max_length=500, blank=False, help_text='Please specify your available time for taking the lessons.')
    lesson_numbers = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, choices=duration_choices,default=1)
    interval = models.PositiveIntegerField(blank=False, choices=interval_choices,default=1)
    further_info = models.CharField(max_length=500, blank=False, help_text='Please provide further information such as what you want to learn or your preferred teacher.')
    approve_status = models.BooleanField(default=False)

    objects = CustomLessonManager()

class ApprovedBooking(models.Model):

    duration_choices = [(1,"30"),(2,"45"),(3,"60")]
    interval_choices = [(1,"1"),(2,"2")]

    student = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    start_date = models.DateField(blank=False)
    day_of_the_week = models.DateTimeField(blank=False)
    lesson_numbers = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, choices=duration_choices)
    interval = models.PositiveIntegerField(blank=False, choices=interval_choices)
    teacher = models.CharField(max_length=50,blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    approve_status = models.BooleanField(default=True)
    
    objects = CustomApprovedBookingManager()

    def total_price(self):
        return self.lesson_numbers * self.price

class Invoice(models.Model):
    lesson_in_invoice = models.OneToOneField(Lesson,on_delete=models.CASCADE,blank=False)
    invoice_num = models.AutoField(primary_key=True)
    balance_due = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_paid = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def invoice_ref_num(self):
        return f'{self.lesson_in_invoice.student.student_ref_num}-{self.invoice_num}'
