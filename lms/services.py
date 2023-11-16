import datetime

from django.utils import timezone

from lms.models import Lesson, Course


def update_course_data(instance, action):
    updated_course = instance
    if isinstance(instance, Lesson):
        updated_course = Course.objects.get(pk=instance.course.pk)

    # update Course filed updated_at
    last_updated_at = updated_course.updated_at
    updated_course.updated_at = timezone.now()
    updated_course.save()

    # launch send_message
    print(last_updated_at) #UTC
    print(timezone.now()) #UTC
    if last_updated_at < (timezone.now() - datetime.timedelta(hours=4)):
        subscription_objects = updated_course.subscription.all()
        for subscription in subscription_objects:
            print(f'Письмо для {subscription.owner.email}: Вы получили рассылку, т.к. подписались на обновления курса '
              f'{updated_course.title}. '
              f'В данном курсе произошли обновления: {action} {instance.title}')
            # SendUpdateMail.delay()
    # else:
    #     print('недавно')

