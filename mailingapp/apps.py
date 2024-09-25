from time import sleep

from django.apps import AppConfig


class MailingappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailingapp'

    def ready(self):
        from mailingapp.services import start
        sleep(2)
        start()
