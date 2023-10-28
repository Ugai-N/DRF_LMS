from django.core.management import BaseCommand

from lms.models import Payment, Course, Lesson
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        payment_list = [
            {'user': User.objects.get(pk=2), 'course': Course.objects.get(pk=1), 'amount_paid': 7000,
             'payment_method': 'CASH'},
            {'user': User.objects.get(pk=2), 'lesson': Lesson.objects.get(pk=7), 'amount_paid': 500,
             'payment_method': 'TT'},
            {'user': User.objects.get(pk=1), 'course': Course.objects.get(pk=2), 'amount_paid': 5000,
             'payment_method': 'CASH'},
            {'user': User.objects.get(pk=1), 'lesson': Lesson.objects.get(pk=6), 'amount_paid': 1200,
             'payment_method': 'TT'},
        ]

        # а вот тут мы сначала все элементы складываем в список, а потом балком отдаем в БД
        payments_to_create = []
        for payment in payment_list:
            payments_to_create.append(Payment(**payment))
        Payment.objects.bulk_create(payments_to_create)
