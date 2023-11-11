from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from lms.models import Lesson
from lms.paginators import CourseLessonPaginator
from lms.permissions import IsModerator, IsStudent
from lms.serializers.lesson import LessonSerializer, LessonListSerializer, LessonCreateSerializer


class LessonListAPIView(ListAPIView):
    serializer_class = LessonListSerializer
    # queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator

    def get_queryset(self, *args, **kwargs):
        queryset = Lesson.objects.all()
        if not self.request.user.groups.filter(name='Модератор').exists():
            queryset = queryset.filter(pk__in=self.request.user.lessons.all())
        return queryset


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsStudent | IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsStudent | IsModerator]


class LessonDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsStudent]
