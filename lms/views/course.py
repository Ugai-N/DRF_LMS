from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from lms.services import update_course_data
from lms.tasks import SendUpdateMail
from lms.models import Course
from lms.paginators import CourseLessonPaginator
from lms.permissions import IsModerator, IsStudent, IsOwner
from lms.serializers.course import CourseSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для Course с динамическим использованием сериалайзера"""
    default_serializer = CourseSerializer
    queryset = Course.objects.all()
    serializers_list = {
        "retrieve": CourseDetailSerializer,
    }
    pagination_class = CourseLessonPaginator

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(~IsModerator)
        if self.action in ['retrieve']:
            permission_classes.append(IsStudent | IsModerator | IsOwner)
        if self.action in ['update', 'partial_update']:
            permission_classes.append(IsModerator | IsOwner)
        if self.action == 'destroy':
            permission_classes.append(IsOwner)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Функия для использования сериализатора в зависимости от action.
        Если запрашиваемого action нет в serializers_list - берется default_serializer"""
        return self.serializers_list.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        """Переопределяем метод list,
        перезаписываем queryset с анотированным полем lessons_count,
        в которое вписываем сущность с related_name=lesson"""

        self.queryset = self.queryset.annotate(lessons_count=Count('lesson'))

        """Выводим список курсов, по которым пользователь является либо учеником, либо автором. Модераторам видны все"""
        if not self.request.user.groups.filter(name='Модератор').exists():
            self.queryset = self.queryset.filter(pk__in=self.request.user.courses.all()) | \
                            self.queryset.filter(owner=self.request.user)
        return super().list(request, *args, **kwargs)

    # инфа по разнице create-perfrom create
    # https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
    # https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        updated_course = serializer.save()
        update_course_data(updated_course, 'Изменен')
