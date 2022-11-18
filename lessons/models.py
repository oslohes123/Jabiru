from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank = False)
    password = models.CharField(max_length=30, blank= False)
# First name
# Last name
# Email
# Password