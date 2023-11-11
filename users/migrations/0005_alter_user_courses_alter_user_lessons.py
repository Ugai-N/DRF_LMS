# Generated by Django 4.2.6 on 2023-11-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_alter_course_owner_alter_lesson_owner'),
        ('users', '0004_alter_user_courses_alter_user_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(related_name='students', to='lms.course', verbose_name='курсы пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lessons',
            field=models.ManyToManyField(related_name='students', to='lms.lesson', verbose_name='уроки пользователя'),
        ),
    ]
