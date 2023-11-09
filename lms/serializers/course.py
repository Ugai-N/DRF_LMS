from rest_framework import serializers
from rest_framework.fields import IntegerField

from lms.models import Course
from lms.serializers.lesson import CourseLessonListSerializer


class CourseSerializer(serializers.ModelSerializer):
    """Дефолтный сериалайзер для всех операций, кроме retrieve, с доп.полем вывода кол-ва уроков в курсе"""
    lessons_count = IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons_count')


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериалайзер для retrieve с выводом данных обо всех уроках, относящихся к курсу"""
    lesson = CourseLessonListSerializer(many=True)

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'lesson')
