from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    message = "У вас недостаточно прав"

    def has_object_permission(self, request, view, obj):
        if request.user in obj.students.all():
        # if obj in request.user.courses.all() or obj in request.user.lessons.all():
            return True
        return False


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модератор').exists():
            return True
        return False
