from django.core.management import BaseCommand

from usersapp.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ Создает суперпользователя"""

        user = User.objects.create(
            email='9232485@gmail.com',
            first_name='Admin',
            last_name='Adminka',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('22021983')
        user.save()
