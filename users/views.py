from django.shortcuts import render
from rest_framework.generics import UpdateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
