import datetime as dt

from rest_framework import serializers
from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year_now = dt.date.today().year
        if not (0 < value <= year_now):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор постов."""

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""

    class Meta:
        fields = '__all__'
        model = Genre
