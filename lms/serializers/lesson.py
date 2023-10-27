from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    """Общий сериалайзер с выводом полной информации об уроке"""
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода сокращенной информации об уроке"""
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'preview', 'course')


class CourseLessonListSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода в курсе сокращенной информации об уроке"""
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'preview')

