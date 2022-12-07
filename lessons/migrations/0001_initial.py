# Generated by Django 4.1.3 on 2022-12-07 19:37

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('role', models.CharField(choices=[('Student', 'Student'), ('Adult', 'Adult student or parent'), ('Administrator', 'Administrator'), ('Director', 'Director')], max_length=13)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApprovedBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('day_of_the_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=20)),
                ('time_of_the_week', models.TimeField()),
                ('total_lessons_count', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField(choices=[(30, '30'), (45, '45'), (60, '60'), (75, '75'), (90, '90'), (105, '105'), (120, '120')])),
                ('interval', models.PositiveIntegerField(choices=[(1, 'weekly interval'), (2, 'fortnightly interval'), (3, 'three-weeks interval'), (4, 'monthly interval')])),
                ('assigned_teacher', models.CharField(max_length=50)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_due', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('lesson_in_invoice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lessons.approvedbooking')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(help_text='Please specify your available time for taking the lessons.', max_length=500)),
                ('total_lessons_count', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField(choices=[(30, '30'), (45, '45'), (60, '60'), (75, '75'), (90, '90'), (105, '105'), (120, '120')], default=30)),
                ('interval', models.PositiveIntegerField(choices=[(1, 'weekly interval'), (2, 'fortnightly interval'), (3, 'three-weeks interval'), (4, 'monthly interval')], default=1)),
                ('further_info', models.CharField(help_text='Please provide further information such as what you want to learn or your preferred teacher.', max_length=500)),
                ('approve_status', models.BooleanField(default=False)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
