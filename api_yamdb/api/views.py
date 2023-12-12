import http

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import (AdminOrReadOnly, IsAuthorOrModerAdminPermission,
                             UserIsAdmin)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User

HTTP_METHOD_WITHOUT_PUT = ('get', 'post', 'patch', 'delete')


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'),
    ).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    http_method_names = HTTP_METHOD_WITHOUT_PUT

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModerAdminPermission,
    )
    http_method_names = HTTP_METHOD_WITHOUT_PUT

    def get_post(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_post())

    def get_queryset(self):
        return self.get_post().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrModerAdminPermission,
    )
    http_method_names = HTTP_METHOD_WITHOUT_PUT

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id, title=title)

    def perform_create(self, serializer):
        """Создание нового коммента."""

        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        """Получение кверисета."""

        return self.get_review().comments.all()


class SignUpAPIView(APIView):
    """Отправляем запрос с именем и почтой. Джанго высылает письмо на почту."""

    def post(self, *args, **kwargs):
        serializer = SignUpSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        try:
            user, _ = User.objects.get_or_create(
                email=email,
                username=username,
            )
        except IntegrityError:
            raise ValidationError(
                detail='Нужно проверить имя пользователя и почту.',
            )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(subject='Подтверждение пользователя',
                  message=f'Код : {confirmation_code}',
                  from_email=settings.SENDER_EMAIL,
                  recipient_list=[user.email])
        return Response({'email': f'{email}',
                         'username': f'{username}'},
                        status=http.HTTPStatus.OK)


class TokenAPIView(APIView):
    """Post запрос пользователя: имя и код подтверждения."""

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': 'Не правильное имя'},
                            status=http.HTTPStatus.NOT_FOUND)

        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=http.HTTPStatus.CREATED)
        return Response({'confirmation_code': 'Не правильный код'},
                        status=http.HTTPStatus.BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователем от имени администратора +"""
    """'GET', 'PATCH' для зарегистрированного пользователя"""

    queryset = User.objects.all()
    permission_classes = (UserIsAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = HTTP_METHOD_WITHOUT_PUT

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=http.HTTPStatus.OK)
