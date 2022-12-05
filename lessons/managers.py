from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, password):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            parent=None
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role, password):
        user = self.create_user(email, first_name, last_name, role, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomLessonManager(BaseUserManager):
    def create_lesson(self, student, availability, lesson_numbers, duration, interval, further_info, approve_status):
        lesson = self.model(
            student=student,
            availability=availability,
            lesson_numbers=lesson_numbers,
            duration=duration,
            interval=interval,
            further_info=further_info,
            approve_status=approve_status,
        )
        lesson.save(using=self._db)
        return lesson
