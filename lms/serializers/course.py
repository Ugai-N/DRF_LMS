from rest_framework import serializers
from rest_framework.fields import IntegerField

from lms.models import Course, Subscription
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
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, instance):
        subscription = [sub for sub in instance.subscription.all() if sub.user == self.context['request'].user]
        if subscription:
            if subscription[0].is_active:
                return f'Подписка активна'
            return f'Ваша подписка неактивна'
        return f'У вас нет подписки на данный продукт'

        # course_subscriptions = instance.subscription.all()
        # for subscription in course_subscriptions:
        #     if subscription.user == self.context['request'].user:
        #         current_user_subscription = subscription
        #         if current_user_subscription.is_active:
        #             return f'Подписка активна'
        #         return f'Ваша подписка неактивна'
        #     return f'У вас нет подписки на данный продукт'

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'subscription', 'lesson')
