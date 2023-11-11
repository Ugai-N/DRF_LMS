
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.CharField(verbose_name='email', unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    phone = models.CharField(verbose_name='телефон', max_length=35, **NULLABLE)
    city = models.CharField(verbose_name='город', max_length=50, **NULLABLE)
    avatar = models.ImageField(verbose_name='аватар', upload_to='users/', **NULLABLE)
    courses = models.ManyToManyField('lms.Course', verbose_name='курсы пользователя', related_name='students', **NULLABLE)
    lessons = models.ManyToManyField('lms.Lesson', verbose_name='уроки пользователя', related_name='students', **NULLABLE)
