from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from lessons.models import User, Lesson
from lessons.constants import *

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker('en_GB')
        Faker.seed(random.randint(0,999999))

    def handle(self, *args, **options):
    
        self.user = User.objects.create_user(
            'john.doe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123',
            role=student
        )

        self.user = User.objects.create_user(
            'petra.pickles@example.org',
            first_name='Petra',
            last_name='Pickles',
            password='Password123',
            role=administrator
        )

        self.user = User.objects.create_user(
            'marty.major@example.org',
            first_name='Marty',
            last_name='Major',
            password='Password123',
            role=director,
        )

        for i in range(0, 100):
            temp_profile = self.fake.simple_profile()
            self.user = User.objects.create_user(
                temp_profile.get("mail"),
                first_name = temp_profile.get("name").split()[0] + " " + temp_profile.get("name").split()[1] if len(temp_profile.get("name").split()) == 3 else temp_profile.get("name").split()[0],
                last_name = temp_profile.get("name").split()[-1],
                password = self.fake.password(length = 12),
                role = student
            )

        #TODO Seeding for lessons for test student -- seed lessons
        self.lesson = Lesson.objects.create_lesson(
            student = User.objects.get(email = 'blah@gha.com'),
            availability = 'From 14:00 to 18:00',
            lesson_numbers = 3,
            duration = 100,
            interval = 2,
            further_info = 'Guitar lessons with Mr.Guitar',
            approve_status = True
        )