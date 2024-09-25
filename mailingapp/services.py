import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from mailingapp.models import Mailing, Attempt


def change_mailing_status():
    """
    Меняет статус рассылки.
    """

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.exclude(status_mailing='completed').exclude(is_disabled=True)

    for mailing in mailings:
        if mailing.end_mailing < current_datetime:
            mailing.status_mailing = 'completed'
            mailing.save(update_fields=['status_mailing'])
        if mailing.status_mailing == 'created' and mailing.start_mailing <= current_datetime:
            mailing.status_mailing = 'launched'
            mailing.save(update_fields=['status_mailing'])


def is_next_send_time(mailing: Mailing, attempt: Attempt, current: datetime) -> bool:
    """
    Проверяет следующее время рассылки.
    """

    time_difference = current - attempt.last_attempt if attempt else 0
    if attempt:
        if mailing.periodic_mailing == 'once a day' and time_difference >= timedelta(days=1):
            return True
        elif mailing.periodic_mailing == 'once a week' and time_difference >= timedelta(days=7):
            return True
        elif mailing.periodic_mailing == 'once a month' and time_difference >= timedelta(days=30):
            return True
    else:
        return True

    return False


def send_mailing():
    """
    Отправляет рассылку.
    """

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status_mailing='launched')

    for mailing in mailings:
        attempts = Attempt.objects.filter(mailing=mailing)
        end_attempt = attempts.order_by('-last_attempt')[0] if attempts else None  # получаем последнюю попытку

        if is_next_send_time(mailing, end_attempt, current_datetime):
            response = ''
            try:
                send_mail(
                    subject=mailing.message.message_title,
                    message=mailing.message.message_text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email_client for client in mailing.clients.all()],
                    fail_silently=False,
                )
                status = 'Successfully'

            except smtplib.SMTPException as e:
                status = 'Not successful'
                response = str(e)

            Attempt.objects.create(
                status_attempt=status,
                answer_mail_server=response,
                mailing=mailing,
                last_attempt=current_datetime,
            )


def start():
    """
    Запускает периодическую задачу.
    """

    scheduler = BackgroundScheduler()
    scheduler.add_job(change_mailing_status, 'interval', seconds=60)
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()
