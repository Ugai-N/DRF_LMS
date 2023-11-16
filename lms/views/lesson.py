from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from lms.models import Lesson
from lms.paginators import CourseLessonPaginator
from lms.permissions import IsModerator, IsStudent, IsOwner
from lms.serializers.lesson import LessonSerializer, LessonListSerializer, LessonCreateSerializer
from lms.services import update_course_data


class LessonListAPIView(ListAPIView):
    serializer_class = LessonListSerializer
    # queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator

    def get_queryset(self, *args, **kwargs):
        """Выводим список уроков, по которым пользователь является либо учеником, либо автором. Модераторам видны все"""
        queryset = Lesson.objects.all()
        if not self.request.user.groups.filter(name='Модератор').exists():
            queryset = queryset.filter(pk__in=self.request.user.lessons.all()) | queryset.filter(owner=self.request.user)
            # queryset = queryset.filter(pk__in=self.request.user.lessons.all())
            # queryset = queryset.filter(owner=self.request.user)
        return queryset.order_by('id')


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Сохраняем текущего пользователя в авторы (owner)"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        update_course_data(new_lesson, 'Создан')


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsStudent | IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        updated_lesson = serializer.save()
        update_course_data(updated_lesson, 'Изменен')


class LessonDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
