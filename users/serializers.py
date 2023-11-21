from tkinter import Entry

from django.contrib.auth.password_validation import validate_password
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


class UserRegisterSerializer(serializers.ModelSerializer):
    """Cериалайзер для регистрации User"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # widget = Entry('password', show="*", width=15)
    # password2 = getpass.getpass()
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
