from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""

    list_display = [
        'email', 'first_name', 'last_name', 'role', 'is_active','id'
    ]

@admin.register(Lesson)
class LessonsAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""

    list_display = [
        'student',
        'availability',
        'total_lessons_count',
        'duration',
        'interval',
        'further_info',
        'approve_status',
        'id'
    ]


@admin.register(ApprovedBooking)
class ApprovedBookingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""

    list_display = [
        'student',
        'start_date',
        'day_of_the_week',
        'total_lessons_count',
        'duration',
        'interval',
        'assigned_teacher',
        'hourly_rate',
        "approve_status",
        'id'
    ]

@admin.register(Invoice)
class LessonsAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""

    list_display = [
        'lesson_in_invoice',
        'balance_due',
        'payment_paid',
        'id'
    ]


@admin.register(Transaction)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = [
        'invoice',
        'payment_amount'
    ]