from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from lessons.models import User

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
            role='Student'
        )

        self.user = User.objects.create_user(
            'petra.pickles@example.org',
            first_name='Petra',
            last_name='Pickles',
            password='Password123',
            role='Administrator'
        )

        self.user = User.objects.create_user(
            'marty.major@example.org',
            first_name='Marty',
            last_name='Major',
            password='Password123',
            role='Director',
        )

        for i in range(0, 100):
            temp_profile = self.fake.simple_profile()
            self.user = User.objects.create_user(
                temp_profile.get("mail"),
                first_name = temp_profile.get("name").split()[0] + " " + temp_profile.get("name").split()[1] if len(temp_profile.get("name").split()) == 3 else temp_profile.get("name").split()[0],
                last_name = temp_profile.get("name").split()[-1],
                password = self.fake.password(length = 12),
                role = 'Student'
            )