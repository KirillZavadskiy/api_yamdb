from django.db import models


class Category(models.Model):
    """Модель Категории."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug Категории', unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug Жанра', unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведени."""

    name = models.CharField('Название', max_length=256,)
    year = models.PositiveSmallIntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        null=True,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name
