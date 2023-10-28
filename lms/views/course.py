from django.db.models import Count
from rest_framework import viewsets

from lms.models import Course
from lms.serializers.course import CourseSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для Course с динамическим использованием сериалайзера"""
    default_serializer = CourseSerializer
    queryset = Course.objects.all()
    serializers_list = {
        "retrieve": CourseDetailSerializer,
    }

    def get_serializer_class(self):
        """Функия для использования сериализатора в зависимости от action.
        Если запрашиваемого action нет в serializers_list - берется default_serializer"""
        return self.serializers_list.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        """Переопределяем метод list,
        перезаписываем queryset с анотированным полем lessons_count,
        в которое вписываем сущность с related_name=lesson"""

        self.queryset = self.queryset.annotate(lessons_count=Count('lesson'))
        return super().list(request, *args, **kwargs)
