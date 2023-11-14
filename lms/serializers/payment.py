from rest_framework import serializers

from lms.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Cериалайзер для всех операций Payment"""

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user',)


class UserPaymentSerializer(serializers.ModelSerializer):
    """Cериалайзер для сокращенного вывода платежей в пользователе с доп.полем product,
    в которое выводим либо название курса, либо название урока, по ктр прошел платеж"""

    product = serializers.SerializerMethodField()
    paid_via = serializers.SerializerMethodField()

    def get_product(self, instance):
        if instance.course:
            return f'курс {instance.course.title}'
        return f'урок {instance.lesson.title} из курса {instance.lesson.course.title}'

    def get_paid_via(self, instance):
        return instance.get_payment_method_display()

    class Meta:
        model = Payment
        fields = ('payment_date', 'amount_paid', 'paid_via', 'product')
