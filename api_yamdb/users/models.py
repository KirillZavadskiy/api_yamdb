from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя.',
        max_length=150,
        blank=True,
        null=True)
    last_name = models.CharField(
        verbose_name='Фамилия.',
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=100,
        choices=USER_ROLES,
        default=USER,
        blank=True
    )
    confirmation_code = models.UUIDField(
        verbose_name='Код',
        null=True,
        max_length=40,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
