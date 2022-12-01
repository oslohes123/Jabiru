from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator
from .managers import CustomUserManager, CustomLessonManager
from .constants import *

role_choices = ((student, 'Student'), (adult, 'Adult student or parent'))


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, max_length=30, blank=False)
    role = models.CharField(max_length=10, choices=role_choices, blank=False)

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


class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    availability = models.CharField(max_length=500, blank=False,
                                    help_text='Please specify your available time for taking the lessons.')  # for students availability
    lesson_numbers = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, validators=[
        MaxValueValidator(240, message='Duration can not be bigger than 240')])
    interval = models.PositiveIntegerField(blank=False, validators=[
        MaxValueValidator(8, message='Interval can not be bigger than 8')])
    further_info = models.CharField(max_length=500, blank=False,
                                    help_text='Please provide further information such as what you want to learn or your preferred teacher.')
    approve_status = models.BooleanField(default=False)
    objects = CustomLessonManager()

    def price(self):
        return self.duration / 60 * 15

    def status_string(self):
        if not self.approve_status:
            return "Not approved"
        else:
            return "Approved"
