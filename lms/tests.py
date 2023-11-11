from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:

        # чтобы залогиниться под пользователем
        # self.user = User(email='777test@yandex.ru')
        # password = 'SyncMaster11'
        # self.user.set_password(password)
        # self.user.save()
        #
        # # Authenticate client with user
        # self.client = APIClient()
        # self.client.login(email=self.user.email, password=password)


        self.client = APIClient()
        self.user = User.objects.create(email='777test@yandex.ru', password='SyncMaster11')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='test_course')
        self.lesson = Lesson.objects.create(title='test_lesson', course=self.course)

    def test_get_list(self): # в одном тесте может быть МАКСИМУМ 1-2 ассерта
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse('lms:lessons'))

        # проверяем что нет ошибок вывода страницы
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверяем структуру вывода

        # self.assertEqual(
        #     response.json(),
        #     {
        #         "count": 1,
        #         "next": None,
        #         "previous": None,
        #         "results": [
        #             {
        #                 "id": 1,
        #                 "title": "test_lesson",
        #                 "preview": None,
        #                 "course": 'test_course'
        #             }
        #         ]
        #     }
        # )

    def test_lesson_create(self):
        """Тестирование создания урока"""

        data = {
            'title': 'test_lesson2',
            'course': self.course.id
        }
        response = self.client.post(reverse('lms:create_lesson'), data=data)
        # print(response.json()['owner'])
        # print(User.objects.get(pk=2).email)
        # print(self.user.email)

        # проверяем что нет ошибок вывода страницы
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # проверяем что после создания теперь 2 урока (один в сетапе)
        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_create_validation(self):
        """Тестирование валидации при создании урока"""

        data = {
            'title': 'test_lesson3',
            'course': self.course.id,
            'video': 'https://www.youtube.com/watch?v=BLtBiAXVsaM',
            'description': 'https://www.google.com/'
        }
        response = self.client.post(reverse('lms:create_lesson'), data=data)

        # проверяем что нет ошибок вывода страницы
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # проверяем что выдается сообщение ктр мы записали
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Недопустимо указание ссылок на любые источники, кроме Youtube']}
        )
