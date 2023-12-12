import re

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def username_validator(value):
    unmatched = re.sub(r'^[\w.@+-]+\Z', '', value)
    if value == 'me':
        raise ValidationError('Нельзя использовать имя "me"')
    elif value in re.sub(r'^[\w.@+-]+\Z', '', value):
        raise ValidationError(
            f'Имя не может включать слудующие знаки: {unmatched}',
        )
    return value


class User(AbstractUser):
    """Модель пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )

    username = models.CharField(
        max_length=settings.USERNAME_LENGTH,
        unique=True,
        validators=(username_validator, ),
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя.',
        max_length=settings.FIRST_NAME_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия.',
        max_length=settings.LAST_NAME_LENGTH,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=settings.ROLE_LENGTH,
        choices=USER_ROLES,
        default=USER,
        blank=True,
    )
    confirmation_code = models.UUIDField(
        verbose_name='Код',
        null=True,
        max_length=40,
        blank=True,
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
