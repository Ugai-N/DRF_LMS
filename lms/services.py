import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule, PeriodicTasks

# def set_schedule(name, every, period, *args, **kwargs):
#     # запускается для сбрасывания часового пояса
#     # PeriodicTask.objects.update(last_run_at=None)
#     # PeriodicTasks.changed()
#
#     schedule, created = IntervalSchedule.objects.get_or_create(
#         every=every,
#         period=IntervalSchedule.PERIOD_CHOICES[period][0],
#     )
#
#     PeriodicTask.objects.create(
#         interval=schedule,  # we created this above.
#         name=name,  # simply describes this periodic task.
#         task='lms.tasks.testing_tasks',  # name of task.
#         args=json.dumps([args[0], args[1]]),
#         kwargs=json.dumps({
#             'title_name': kwargs['title'],
#         }),
#         # expires=datetime.utcnow() + timedelta(seconds=30)
#     )


def set_schedule(task_name, every, period, start_at, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=every,
        period=IntervalSchedule.PERIOD_CHOICES[period][0],
    )

    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name=task_name,  # simply describes this periodic task.
        task='lms.tasks.testing_tasks',  # name of task.
        # args=json.dumps([args[0], args[1]]),
        kwargs=json.dumps({
            'text1': kwargs['text1'],
            'text2': kwargs['text2'],
            'title_name': kwargs['title'],
        }),
        start_time=start_at,
        # expires=datetime.utcnow() + timedelta(seconds=30)
    )


def disable_task():
    needed_task = PeriodicTask.objects.get(name='course 7')
    needed_task.enabled = False
    needed_task.save()
