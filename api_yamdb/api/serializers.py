import re

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Базовый сериализатор модели Title."""

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )

    def validate_year(self, value):
        """Проверка года на будущее время."""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Некорректно указан год выпуска.',
            )
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведения для чтения."""

    rating = serializers.IntegerField(read_only=True, default=0)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category',
        )


class TitleWriteSerializer(TitleSerializer):
    """Сериализатор произведения для записи."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            'title',
        )

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.',
            )
        return data

    def validate_score(self, value):
        """Проверка, что оценка в диапазоне от 1 до 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка может быть от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для аyтэнтификации. Использует username, email."""

    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=settings.USERNAME_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Нельзя использовать имя: "me".')
        return username


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для получения токена. Использует confirmation_code.
    Если питест не съест еще имя пользователя придется использовать.
    """
    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_LENGTH,
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CON_CODE_LENGTH,
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
