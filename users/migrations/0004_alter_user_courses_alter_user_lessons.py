# Generated by Django 4.2.6 on 2023-11-11 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_course_owner_lesson_owner'),
        ('users', '0003_user_courses_user_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to='lms.course', verbose_name='курсы пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lessons',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to='lms.lesson', verbose_name='уроки пользователя'),
        ),
    ]
