from rest_framework import serializers

from lms.models import Lesson
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
