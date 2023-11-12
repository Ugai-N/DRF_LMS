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

        course = Course.objects.create(title='test_course')
        lesson = Lesson.objects.create(title='test_lesson', course=course)

    def test_setup(self):
        """Тестирование создание урока в SetUp - OK"""

        lesson = Lesson.objects.get(title='test_lesson')

        # проверяем что в базе появился новый урок
        self.assertEqual(lesson.course.title, 'test_course')

        # проверяем что владелец новому уроку не присвоился
        self.assertEqual(lesson.course.owner, None)

        # проверяем что в базе всего 1 курс
        self.assertEqual(
            Lesson.objects.all().count(),
            1
        )
        # проверяем что в базе появился 1 урок
        self.assertEqual(
            Course.objects.all().count(),
            1
        )

    def test_ownerfield_lesson_create(self):
        """Тестирование создания урока"""
        data = {
            'title': 'test_lesson2',
            'course': 1
        }
        response = self.client.post(reverse('lms:create_lesson'), data=data)

        # проверяем, что нет ошибок вывода страницы
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # проверяем, что owner - пользователь, установленный в сетапе
        self.assertEqual(Lesson.objects.get(title='test_lesson2').owner.email, '777test@yandex.ru')

    def test_get_list(self):
        """Тестирование вывода списка уроков, где пользователь владелец"""

        data = {
            'title': 'test_lesson2',
            'course': 1
        }
        create_response = self.client.post(reverse('lms:create_lesson'), data=data)

        list_response = self.client.get(reverse('lms:lessons'))

        # проверяем что нет ошибок вывода страницы
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        # проверяем, что пользователю выведется только 1 урок, где он - владелец
        self.assertEqual(len(list_response.json()['results']), 1)

        # проверяем структуру вывода
        self.assertEqual(
            list_response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 2,
                        "title": "test_lesson2",
                        "preview": None,
                        "course": 'test_course'
                    }
                ]
            }
        )

        # print('курс создан в сетапе')
        # print(Course.objects.all().first().title)
        # print(Course.objects.all().first().owner) #None
        # print('урок создан в сетапе')
        # print(Lesson.objects.get(title='test_lesson').pk)
        # print(Lesson.objects.get(title='test_lesson').owner) #None
        #
        # print('урок создан в тесте')
        # print(Lesson.objects.get(title='test_lesson2').pk)
        # print(Lesson.objects.get(title='test_lesson2').owner) # 777test@yandex.ru

    def test_get_student_list(self):
        """Тестирование вывода списка уроков (где пользователь - ученик)"""

        # присваиваем пользователю статус ученика по уроку, установленному в сетапе (pk=1)
        self.user.lessons.set([1])
        self.user.save()

        list_response = self.client.get(reverse('lms:lessons'))

        # проверяем что нет ошибок вывода страницы
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        # проверяем, что пользователю выведется только 1 урок (где он - ученик) с названием test_lesson (pk=1)
        self.assertEqual(list_response.json()['results'][0]['title'], 'test_lesson')

    def test_student_lesson_update(self):
        """Тестирование невозможности редактировать уроки студентом"""

        # присваиваем пользователю статус ученика по уроку, установленному в сетапе (pk=1)
        self.user.lessons.set([1])
        self.user.save()

        data = {
            'title': 'test_lesson_upd'
        }
        response = self.client.patch('/lessons/1/edit/', data=data)
        print(response.content)

        # проверяем, что у пользователя нет прав
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_lesson_update(self):
        """Тестирование возможности редактировать уроки владельцем"""

        create_data = {
            'title': 'test_lesson2',
            'course': 1
        }
        create_response = self.client.post(reverse('lms:create_lesson'), data=create_data)

        update_data = {
            'title': 'test_lesson_upd'
        }
        update_response = self.client.patch('/lessons/2/edit/', data=update_data)

        # проверяем, что нет ошибок
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        # проверяем, что название урока изменилось
        self.assertEqual(Lesson.objects.get(pk=2).title, 'test_lesson_upd')

    def test_owner_lesson_delete(self):
        """Тестирование возможности удалять уроки владельцем"""

        create_data = {
            'title': 'test_lesson2',
            'course': 1
        }
        create_response = self.client.post(reverse('lms:create_lesson'), data=create_data)

        delete_response = self.client.delete('/lessons/2/delete/')

        # проверяем, что нет ошибок
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # проверяем, что в БД 1 урок
        self.assertEqual(Lesson.objects.all().count(), 1)
