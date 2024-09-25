from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = None
    email = models.EmailField(verbose_name='электронный адрес', unique=True)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    is_block = models.BooleanField(
        verbose_name='заблокирован',
        **NULLABLE,
        default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("сan_block_user", "Сan block user"),
        ]
        ordering = ['-id']
