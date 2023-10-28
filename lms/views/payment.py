from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from lms.models import Payment
from lms.serializers.payment import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Payment с возможностью фильтрации по курсу, уроку и методу оплаты,
    а также возможностью сортировки по дате оплаты"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)
