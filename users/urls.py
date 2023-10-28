from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView

app_name = UsersConfig.name
urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('', UserListAPIView.as_view(), name='list_user'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='view_user'),
    # path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('profile/', UserUpdateAPIView.as_view(), name='edit_profile'),
]
