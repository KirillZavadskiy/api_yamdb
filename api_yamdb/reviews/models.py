from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year
from users.models import User


class CategoryGenreModel(models.Model):
    """Абстрактная модель для категорий и жанров."""

    name = models.CharField(
        'Название',
        max_length=settings.NAME_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('slug',)

    def __str__(self):
        return self.slug[:settings.AMT_SIGN_TITLE]


class Category(CategoryGenreModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название произведения',
        max_length=settings.NAME_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        null=True,
        validators=(validate_year,),
    )
    description = models.TextField(
        'Описание произведения',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year',)

    def __str__(self):
        """Возвращает название произведения."""
        return self.name[:settings.AMT_SIGN_TITLE]


class GenreTitle(models.Model):
    """Связь жанра и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title',
            ),
        )

    def __str__(self):
        return f'{self.title} {self.genre}'[:settings.AMT_SIGN_TITLE]


class ReviewCommentModel(models.Model):
    """Абстрактная модель для отзывов и комментариев."""

    text = models.TextField('текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.AMT_SIGN_TITLE]


class Review(ReviewCommentModel):
    """Модель ревью (отзывы на произведения)."""

    score = models.PositiveSmallIntegerField(
        'Оценка',
        default=None,
        validators=(
            MinValueValidator(
                1,
                message='Оценка меньше допустимой',
            ),
            MaxValueValidator(
                10,
                message='Оценка больше допустимой',
            ),
        ),
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review',
            ),
        )


class Comment(ReviewCommentModel):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
