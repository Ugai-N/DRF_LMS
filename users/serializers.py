from rest_framework import serializers

from lms.serializers.payment import UserPaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Cериалайзер для User"""
    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """Cериалайзер для метода детального просмотра User с доп.полем payment,
    в которое выводим список всех платежей пользователя"""
    payment = UserPaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
