from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.stripe_services import my_webhook_view
from lms.views.course import CourseViewSet
from lms.views.lesson import LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView
from lms.views.payment import PaymentViewSet
from lms.views.subscription import SubscriptionCreateAPIView, SubscriptionDeleteAPIView

app_name = LmsConfig.name
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
                  path('lessons/', LessonListAPIView.as_view(), name='lessons'),
                  path('lessons/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
                  path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='view_lesson'),
                  path('lessons/<int:pk>/edit/', LessonUpdateAPIView.as_view(), name='edit_lesson'),
                  path('lessons/<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='delete_lesson'),
                  path('subscribe/', SubscriptionCreateAPIView.as_view(), name='subscribe'),
                  path('<int:pk>/unsubscribe/', SubscriptionDeleteAPIView.as_view(), name='unsubscribe'),
                  path('webhook/', my_webhook_view, name='webhook')
              ] + router.urls
