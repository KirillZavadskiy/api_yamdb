from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import IsAdminUserOrReadOnly
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)


class CategoryViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """Получаем посты."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
