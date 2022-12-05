from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, password):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
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
    def create_lesson(self, student, availability, total_lessons_count, duration, interval, further_info,
                      approve_status):
        lesson = self.model(
            student=student,
            availability=availability,
            total_lessons_count=total_lessons_count,
            duration=duration,
            interval=interval,
            further_info=further_info,
            approve_status=approve_status,
        )
        lesson.save(using=self._db)
        return lesson


class CustomApprovedBookingManager(BaseUserManager):
    def create_approvedBooking(self, student, start_date, day_of_the_week, time_of_the_week, total_lessons_count,
                               duration, interval, assigned_teacher, hourly_rate):
        approvedBooking = self.model(
            student=student,
            start_date=start_date,
            day_of_the_week=day_of_the_week,
            time_of_the_week=time_of_the_week,
            total_lessons_count=total_lessons_count,
            duration=duration,
            interval=interval,
            assigned_teacher=assigned_teacher,
            hourly_rate=hourly_rate,
        )
        approvedBooking.save(using=self._db)
        return approvedBooking
