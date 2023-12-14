from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import username_validator


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
        validators=(username_validator,),
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Роль',
        max_length=settings.ROLE_LENGTH,
        choices=USER_ROLES,
        default=USER,
        blank=True,
    )
    confirmation_code = models.UUIDField(
        'Код',
        null=True,
        max_length=settings.CON_CODE_LENGTH,
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
