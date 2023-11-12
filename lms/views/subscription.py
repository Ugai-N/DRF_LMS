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
        new_subscription.owner = self.request.user
        new_subscription.is_active = True
        new_subscription.save()


class SubscriptionDeleteAPIView(DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
