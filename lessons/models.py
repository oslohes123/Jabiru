from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator
from .managers import CustomUserManager,CustomLessonManager

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
    student = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    availability = models.CharField(max_length=500, blank=False, help_text='Please specify your available time for taking the lessons.')
    lesson_numbers = models.PositiveIntegerField(blank=False)
    duration = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(240,message='Duration can not be bigger than 240')])
    interval = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(8,message='Interval can not be bigger than 8')])
    further_info = models.CharField(max_length=500, blank=False, help_text='Please provide further information such as what you want to learn or your preferred teacher.')
    approve_status = models.BooleanField(default=False)

    objects = CustomLessonManager()