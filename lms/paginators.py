from rest_framework.pagination import PageNumberPagination


class CourseLessonPaginator(PageNumberPagination):
    page_size = 3
