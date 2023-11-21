import http
import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from .permissions import UserIsAdmin
from .serializers import (
    SignUpSerializer, TokenSerializer, UserSerializer
)


User = get_user_model()


class SignUpAPIView(APIView):
    """Отправляем запрос с именем и почтой. Джанго высылает письмо на почту."""

    def post(self, *args, **kwargs):
        print(*args, **kwargs)
        serializer = SignUpSerializer(data=self.request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        try:
            user, _ = User.objects.get_or_create(
                email=email,
                username=username
            )
        except IntegrityError:
            raise ValidationError(
                detail='Нужно проверить имя пользователя и почту'
            )

        confirmation_code = self.make_token(user)

        send_mail(subject='Подтверждение пользователя',
                  message=f'Код : {confirmation_code}',
                  from_email='new@yamdb.ru',
                  recipient_list=[user.email])
        return Response({'email': f'{email}',
                         'username': f'{username}'},
                        status=http.HTTPStatus.OK)

    @staticmethod
    def make_token(user: User) -> uuid.UUID:
        """Создаем код подтверждения и сохраняем в модели юзера."""
        confirmation_code: uuid.UUID = uuid.uuid4()
        user.confirmation_code = confirmation_code
        user.save()
        return confirmation_code


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
    http_method_names = ['get', 'post', 'patch', 'delete']

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
        return Response(serializer.data)
