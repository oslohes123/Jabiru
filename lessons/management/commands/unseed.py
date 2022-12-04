from django.core.management.base import BaseCommand, CommandError
from lessons.models import User,Lesson,ApprovedBooking,Invoice

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        ApprovedBooking.objects.all().delete()
        Invoice.objects.all().delete()

