from django.conf import settings
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from lms.models import Payment
from lms.serializers.payment import PaymentSerializer

import stripe

stripe.api_key = settings.STRIPE_API_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Payment с возможностью фильтрации по курсу, уроку и методу оплаты,
    а также возможностью сортировки по дате оплаты"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)

    def create(self, request, *args, **kwargs):
        # Создаем сессию в Stripe (хорошо бы это вынести в stripe_services.py)
        checkout_session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        # вместо product_data можно просто указать product -> product_ID если его создавать при
                        # создании уроков и курсов + сохранять в модели продукта)
                        "product_data": {
                            "name": "lesson 3", # print(request.data['product'])   # print(self.get_serializer.data['product'])
                            "description": "lesson 3 description"
                        },
                        "unit_amount": request.data['amount_paid']  # можно делать ретрив из ID продукта
                        # с дефолтной ценой
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            # ui_mode='hosted'
        )

        # Заполняем нужные поля в Платеже касательно Stripe сессии
        request.data['payment_link'] = checkout_session.url
        request.data['payment_session_stripe_id'] = checkout_session.id

        # Заполняем поле плательщита в Платеже и добавляем пользователю курсы ученика
        request.data['user'] = self.request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # return HttpResponseRedirect(checkout_session.url)
