from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для аyтэнтификации. Использует username, email."""
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Нельзя использовать имя: "me".')
        return username


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена. Использует confirmation_code.""
     "" Если питест не съест еще имя пользователя придется использовать."""
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']
