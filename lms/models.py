from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='course_preview/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name='название')
    preview = models.ImageField(upload_to='lesson_preview/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    video = models.CharField(max_length=250, verbose_name='ссылка', **NULLABLE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс')
