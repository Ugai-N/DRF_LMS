from celery import shared_task


@shared_task
def SendUpdateMail():
    pass
    # dog_list = Dog.objects.filter(birth=datetime.date.today())
    # for dog in dog_list:
    #     print('dog.name')