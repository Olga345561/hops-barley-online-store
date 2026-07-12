"""Custom user model: email is the login identifier (the design has no username)."""

from typing import Any

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager["User"]):
    """Менеджер, який створює користувачів за електронною поштою, а не за іменем користувача."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields: Any) -> "User":  #створення користувача
        if not email:
            raise ValueError("Потрібно встановити адресу електронної пошти email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "User":
        """Створити звичайного ((non-staff) нештатного) користувача. """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "User":
        """Створення користувача-адміністратора з повними правами доступу."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Клієнт магазину. Входить за допомогою електронної пошти; поля профілю відповідають полю облікового запису."""

    username = None  # type: ignore[assignment]
    email = models.EmailField("email address", unique=True)
    phone = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=128, blank=True)
    address = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # тип: ігнорувати[різне]

    def __str__(self) -> str:
        return self.email

    @property
    def avatar_index(self) -> int:
        """Детермінований індекс від 1 до 10, який використовується для вибору SVG-файлу аватара для відгуку."""
        return (self.pk or 0) % 10 + 1