from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from rest_framework import viewsets
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #filters по всем полям


class CategoryViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #serch по name