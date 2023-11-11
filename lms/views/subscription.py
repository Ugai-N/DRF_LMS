# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import viewsets
#
# from lms.models import Subscription
#
#
#
# class SubscriptionViewSet(viewsets.ModelViewSet):
#     """Вьюсет для Subscription с возможностью фильтрации по курсу, пользователю"""
#     serializer_class = SubscriptionSerializer
#     queryset = Subscription.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ('course', 'user')
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from lms.models import Subscription
from lms.serializers.subscription import SubscriptionSerializer


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Сохраняем текущего пользователя подписку"""
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()


class SubscriptionDeleteAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]