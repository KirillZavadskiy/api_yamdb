from django.db import models


class GenreTitle(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )


class Category(models.Model):
    """Модель Категории."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug Категории', unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Slug Жанра', unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведени."""

    name = models.CharField('Название', max_length=256,)
    year = models.SmallIntegerField('Год выпуска')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        through=GenreTitle,
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name
