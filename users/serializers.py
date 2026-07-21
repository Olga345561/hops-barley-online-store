from typing import Any
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Створіть обліковий запис з електронної пошти + пароля."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password"]
        read_only_fields = ["id"]

    def validate_password(self, value: str) -> str:
        # Тут викликається функція перевірки складності пароля (або вбудовані правила Django)
        validate_password(value)
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        # Створення користувача через метод моделі, щоб пароль правильно хешувався
        return User.objects.create_user(**validated_data)