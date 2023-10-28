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
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс', related_name='lesson')


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Наличные'),
        ('TT', 'Перевод на счет')
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='плательщик', related_name='payment')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс', related_name='payment',
                               **NULLABLE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, verbose_name='урок', related_name='payment',
                               **NULLABLE)
    amount_paid = models.IntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=150, choices=PAYMENT_CHOICES, verbose_name='метод оплаты')
