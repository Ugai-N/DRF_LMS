from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
