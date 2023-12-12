from django.contrib import admin
from django.db.models import Avg
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

admin.site.empty_value_display = 'Значение отсутствует'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель категории в админке."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Модель жанра в админке."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)


class GenreInline(admin.TabularInline):
    """Инлайн для работы с жанрами произведения в админке."""

    model = GenreTitle
    extra = 2


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Модель произведения в админке."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_rating',
        'display_genre',
    )
    inlines = (
        GenreInline,
    )
    list_filter = ('name',)
    list_editable = ('category',)

    @admin.display(description='Рейтинг',)
    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        if (r := rating.get('average_score')) is not None:
            return round(r, 1)
        return r

    @admin.display(description='Жанр',)
    def display_genre(self, object):
        return ' ,'.join((genre.name for genre in object.genre.all()))


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Связанные модели Жанр/произведение в админке."""

    list_display = (
        'pk',
        'genre',
        'title',
    )
    list_filter = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Модель отзывов в админке."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title',
    )
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель комментариев в админке."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review',
    )
    list_filter = ('author', 'pub_date')
    search_fields = ('author',)
