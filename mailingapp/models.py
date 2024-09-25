from django.db import models

from usersapp.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель: клиент сервиса.
    """

    email_client = models.EmailField(verbose_name='электронный адрес', unique=True)
    first_name = models.CharField(max_length=100, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name='фамилия', **NULLABLE)
    middle_name = models.CharField(max_length=100, verbose_name='отчество', **NULLABLE)
    comment_client = models.TextField(verbose_name="комментарий", **NULLABLE)

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        **NULLABLE,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (e-mail: {self.email_client})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['id']


class Mailing(models.Model):
    """
    Модель: рассылка.
    """

    PERIODS = (
        ('once a day', 'раз в день'),
        ('once a week', 'раз в неделю'),
        ('once a month', 'раз в месяц'),
    )
    STATUSES = (
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('completed', 'завершена'),
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания")
    start_mailing = models.DateTimeField(verbose_name="дата и время 1 отправки рассылки")
    end_mailing = models.DateTimeField(verbose_name="дата и время окончания рассылки")
    periodic_mailing = models.CharField(
        verbose_name='периодичность рассылки',
        choices=PERIODS,
        default='раз в день',
    )
    status_mailing = models.CharField(
        verbose_name='статус рассылки',
        choices=STATUSES,
        default='created',
    )
    clients = models.ManyToManyField(
        Client,
        related_name='mailings',
        verbose_name='клиенты сервиса',
        )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        **NULLABLE,
        on_delete=models.SET_NULL
    )
    is_disabled = models.BooleanField(
        verbose_name='отключена менеджером',
        **NULLABLE,
        default=False
    )

    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name='сообщение',
    )

    def __str__(self):
        return f"Рассылка: {self.pk}, создана: {self.created_at}, статус: {self.status_mailing}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("сan_disabled_mailings", "Сan disabled mailings"),
        ]
        ordering = ['-id']


class Message(models.Model):
    """
    Модель: сообщение для рассылки.
    """

    message_title = models.CharField(max_length=200, verbose_name='тема письма')
    message_text = models.TextField(verbose_name="тело письма")
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        **NULLABLE,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Сообщение для рассылки: {self.message_title}"

    class Meta:
        verbose_name = "Сообщение для рассылки"
        verbose_name_plural = "Сообщения для рассылок"
        ordering = ['-id']


class Attempt(models.Model):
    """
    Модель: попытка рассылки.
    """

    ATTEMPTS = (
        ('Successfully', 'успешно'),
        ('Not successful', 'не успешно'),
    )
    last_attempt = models.DateTimeField(verbose_name="дата и время последней попытки")
    status_attempt = models.CharField(
        verbose_name='статус попытки рассылки',
        choices=ATTEMPTS,
        **NULLABLE,
    )
    answer_mail_server = models.TextField(
        verbose_name='ответ почтового сервера',
        **NULLABLE,
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="рассылка",
        **NULLABLE,
    )

    def __str__(self):
        return f"Попытка рассылки: {self.pk},  статус: {self.status_attempt}, последний раз: {self.last_attempt}"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ['-id']
