from celery import shared_task

import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from lms.models import Lesson, Course


@shared_task
# def update_course_data(instance, action):
#     updated_course = instance
#     if isinstance(instance, Lesson):
def update_course_data(pk, model, action):
    if model == 'Lesson':
        updated_lesson = Lesson.objects.get(pk=pk)
        updated_course = Course.objects.get(pk=updated_lesson.course.pk)
    else:
        updated_lesson = None
        updated_course = Course.objects.get(pk=pk)

    # update Course filed updated_at
    last_updated_at = updated_course.updated_at
    updated_course.updated_at = timezone.now()
    updated_course.save()

    # launch send_message
    print(last_updated_at)  # UTC
    print(timezone.now())  # UTC
    # if last_updated_at > (timezone.now() - datetime.timedelta(seconds=4)):
    subscription_objects = updated_course.subscription.all()
    email_list = [subscription.owner.email for subscription in subscription_objects]
    print(email_list)
    print(email_list)
    send_mail(
            subject=f"Обновления курса {updated_course.title}",
            message=f'Вы получили рассылку, т.к. подписались на обновления курса {updated_course.title}.'
                    f'В данном курсе произошли обновления: {action} {updated_lesson.title if updated_lesson else updated_course}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list)

    # else:
    #     print('недавно')
