from django.contrib import admin

from lms.models import Lesson, Course, Payment, Subscription
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'email', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'phone', 'city', 'avatar')
    list_filter = ('is_superuser', 'is_staff', 'is_active',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course', 'owner')
    list_filter = ('course', 'owner')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'updated_at')
    list_filter = ('owner',)
    ordering = ('title',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'amount_paid', 'payment_date', 'payment_method')
    list_filter = ('user', 'course', 'lesson',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'course', 'is_active')
    list_filter = ('owner', 'course', 'is_active')
