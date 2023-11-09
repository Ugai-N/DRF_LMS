from django.contrib import admin

from lms.models import Lesson, Course, Payment
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'avatar', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_staff',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course',)
    list_filter = ('course',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'amount_paid', 'payment_date', 'payment_method')
    list_filter = ('user', 'course', 'lesson',)
