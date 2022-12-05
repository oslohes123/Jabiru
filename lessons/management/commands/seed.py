from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from lessons.models import User, Lesson, ApprovedBooking
from lessons.constants import *
import faker.providers


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker('en_GB')
        Faker.seed(random.randint(0, 999999))

    def handle(self, *args, **options):

        fake_lesson = Faker()
        fake_lesson.add_provider(Provider)

        self.user = User.objects.create_superuser(
            'super@super.com',
            first_name='Super',
            last_name='Duper',
            password='Password123',
            role=director
        )

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

        def setup_user(insert_role):
            self.user = User.objects.create_user(
                temp_profile.get("mail"),
                first_name=temp_profile.get("name").split()[0] + " " + temp_profile.get("name").split()[1] if len(
                    temp_profile.get("name").split()) == 3 else temp_profile.get("name").split()[0],
                last_name=temp_profile.get("name").split()[-1],
                password=self.fake.password(length=12),
                role = insert_role
            )

        def setup_lesson_for_student(email,info_data):
            self.lesson = Lesson.objects.create_lesson(
                student=User.objects.get(email=email),
                # work on this to be of the students emails
                availability=fake_lesson.available_time(),
                total_lessons_count=random.randint(1, 200),
                duration=fake_lesson.duration_time(),
                interval=fake_lesson.interval_choices(),
                further_info=info_data,
                approve_status=False
            )
        
        def setup_approved_lessons(email):
            teacher_name = fake_lesson.teacher_name()
            self.approved_booking = ApprovedBooking.objects.create_approvedBooking(
                student=User.objects.get(email=email),
                start_date=self.fake.future_date(),
                day_of_the_week=self.fake.day_of_week(),
                time_of_the_week = self.fake.time(),
                total_lessons_count=random.randint(1, 200),
                duration=fake_lesson.duration_time(),
                interval=fake_lesson.interval_choices(),
                assigned_teacher=teacher_name,
                hourly_rate= 10.00 , #done 10 as for now change later 
                )


        for i in range(0, 75):
            temp_profile = self.fake.simple_profile()
            setup_user(student)
            # For lessons
            if bool(random.getrandbits(1)):
                instrument = fake_lesson.lesson_instrument()
                teacher = fake_lesson.teacher_name()
                info = instrument + ' lesson with ' + teacher
                #print(temp_profile.get('mail'))
                setup_lesson_for_student(temp_profile.get("mail"),info)
                setup_approved_lessons(temp_profile.get("mail"))

        setup_lesson_for_student("john.doe@example.org",info)
        setup_lesson_for_student("john.doe@example.org",info)
        setup_approved_lessons("john.doe@example.org")
        setup_approved_lessons("john.doe@example.org")

        for i in range(0, 25):
            temp_profile = self.fake.simple_profile()
            setup_user(administrator)


# Lists

DURATION = [
    30,
    45,
    60
]

INTERVAL =[
    1,
    2
]


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
    
    def duration_time(self):
        return self.random_element(DURATION)
    
    def interval_choices(self):
        return self.random_element(INTERVAL)

