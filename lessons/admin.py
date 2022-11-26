from django.contrib import admin
from .models import User,Lesson

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""

    list_display = [
        'email', 'first_name', 'last_name', 'role', 'is_active'
    ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display =[
        'further_info','student','availability','lesson_numbers','duration',
        'interval','approve_status'
    ]
