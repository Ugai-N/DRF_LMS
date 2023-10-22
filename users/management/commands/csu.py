from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='777briz@mail.ru',
            first_name='NN',
            last_name='UU',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('SyncMaster11')
        user.save()
