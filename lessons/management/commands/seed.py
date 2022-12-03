from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from lessons.models import User, Lesson
from lessons.constants import *
import faker.providers


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker('en_GB')
        Faker.seed(random.randint(0, 999999))

    def handle(self, *args, **options):

        self.user = User.objects.create_user(
            'john.doe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123',
            role=student,
            parent=None
        )

        self.user = User.objects.create_user(
            'petra.pickles@example.org',
            first_name='Petra',
            last_name='Pickles',
            password='Password123',
            role=administrator,
            parent=None
        )

        self.user = User.objects.create_user(
            'marty.major@example.org',
            first_name='Marty',
            last_name='Major',
            password='Password123',
            role=director,
            parent=None
        )

        fake_lesson = Faker()
        fake_lesson.add_provider(Provider)

        for i in range(0, 75):
            temp_profile = self.fake.simple_profile()
            self.user = User.objects.create_user(
                temp_profile.get("mail"),
                first_name=temp_profile.get("name").split()[0] + " " + temp_profile.get("name").split()[1] if len(
                    temp_profile.get("name").split()) == 3 else temp_profile.get("name").split()[0],
                last_name=temp_profile.get("name").split()[-1],
                password=self.fake.password(length=12),
                role=student,
                parent=None
            )
            # For lessons
            if bool(random.getrandbits(1)):
                instrument = fake_lesson.lesson_instrument()
                teacher = fake_lesson.teacher_name()
                info = instrument + ' lesson with ' + teacher

                self.lesson = Lesson.objects.create_lesson(
                    student=User.objects.get(email=temp_profile.get("mail")),
                    # work on this to be of the students emails
                    availability=fake_lesson.available_time(),
                    lesson_numbers=random.randint(1, 200),
                    duration=random.randint(1, 240),
                    interval=random.randint(1, 8),
                    further_info=info,
                    approve_status=False
                )

        for i in range(0, 25):
            temp_profile = self.fake.simple_profile()
            self.user = User.objects.create_user(
                temp_profile.get("mail"),
                first_name=temp_profile.get("name").split()[0] + " " + temp_profile.get("name").split()[1] if len(
                    temp_profile.get("name").split()) == 3 else temp_profile.get("name").split()[0],
                last_name=temp_profile.get("name").split()[-1],
                password=self.fake.password(length=12),
                role=administrator,
                parent=None
            )


# Lists

TEACHER_NAME = [
    "Mr. Guitar",
    "Mrs. Doe",
    "Mr. Smiths",
    "Mr. Octo",
    "Mrs. Waer",
    "Mr. Funk",
    "Mrs. Jazz",
    "Mr. Disco",
    "Mrs. Emo"
]

INSTRUMENT = [
    "Guitar",
    "Piano",
    "Drums",
    "Banjo",
    "Harp",
    "Electric Guitar",
    "Bass Guitar",
    "Singing",
    "Flute"
]

AVAILABILITY = [
    "From 10:00 to 18:00",
    "From 14:00 to 18:00",
    "From 10:00 to 12:00",
    "From 10:00 to 15:00",
    "From 11:00 to 18:00",
    "From 09:00 to 16:00",
    "From 12:00 to 17:00"
]


class Provider(faker.providers.BaseProvider):
    def teacher_name(self):
        return self.random_element(TEACHER_NAME)  # TEACHER_NAME being the list of all the teachers

    def lesson_instrument(self):
        return self.random_element(INSTRUMENT)  # INSTRUMENT being a list of all the instruments

    def available_time(self):
        return self.random_element(AVAILABILITY)  # AVAILABILITY being a list of all available times the student can do
