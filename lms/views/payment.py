from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from lms.models import Payment
from lms.serializers.payment import PaymentSerializer

import stripe

stripe.api_key = "sk_test_51OCGbfHWVz8QZA3p7QRKPlnOZ7534HjLmm3rSn6bBkSZwzNcqDlrej6OevRJYGUd3UeXyHWlr00ZkaSgflu1iRHl00fd9TQUN0"


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Payment с возможностью фильтрации по курсу, уроку и методу оплаты,
    а также возможностью сортировки по дате оплаты"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)

    def create(self, request, *args, **kwargs):

        # response = stripe.PaymentIntent.create(
        #     amount=request.data['amount_paid'],
        #     currency="eur",
        #     automatic_payment_methods={"enabled": True},
        #
        # )
        # print(response.id)

        checkout_session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        # вместо product_data можно просто указать product -> product_ID если его создавать при
                        # создании уроков и курсов + сохранять в модели продукта)
                        "product_data": {
                            "name": "lesson 3",
                            "description": "lesson 3 description"
                        },
                        "unit_amount": request.data['amount_paid'] # можно делать ретрив из ID продукта
                        # с дефолтной ценой
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        request.data['payment_link'] = checkout_session.url
        # print(checkout_session.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
