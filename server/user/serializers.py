from typing import Dict

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        # Пароль не будет возвращаться в ответе
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
    
    def validate_password(self, value):
        # Стандартная валидация пароля Django
        validate_password(value)
        return value

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