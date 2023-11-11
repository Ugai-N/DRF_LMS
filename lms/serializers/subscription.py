from rest_framework import serializers

from lms.models import Subscription


# class SubscriptionSerializer(serializers.ModelSerializer):
#     """Cериалайзер для Subscription"""
#
#     class Meta:
#         model = Subscription
#         fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для Subscription"""

    class Meta:
        model = Subscription
        fields = '__all__'
