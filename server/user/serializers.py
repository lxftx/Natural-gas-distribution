from typing import Dict

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели User.
    """

    class Meta:
        model = User
        fields = []
        extra_fields = {
            "email": {
                "min_length": 1,
                "max_length": 255,
                "help_text": "Email адрес",
            },
            "first_name": {
                "min_length": 1,
                "max_length": 64,
                "help_text": "Имя пользователя",
            },
            "last_name": {
                "min_length": 1,
                "max_length": 64,
                "help_text": "Фамилия пользователя",
            },
        }
        read_only_fields = ["created_at", "is_active", "is_staff"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
    
    def validate_password(self, value):
        # Стандартная валидация пароля Django
        validate_password(value)
        return value

class UserDetailSerializer(UserBaseSerializer):
    """
    Сериализатор модели User для детального просмотра расчетов.
    """

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ["email", "first_name", "last_name"]

class UserCreateSerializer(UserBaseSerializer):
    """
    Сериализатор модели User для создания расчета. 
    """
    
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ["email", "first_name", "last_name", "password"]
        # Пароль не будет возвращаться в ответе
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_tokens(cls, user: User) -> Dict[str, str] :
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
