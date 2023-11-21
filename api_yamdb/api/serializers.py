from rest_framework import serializers
from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""

    class Meta:
        fields = '__all__'
        model = Title


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
