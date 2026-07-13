from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Облікові записи: налаштована модель користувача з входом через електронну пошту."""

    default_auto_field = "django.db.models.BigAutoField" #BigAutoField збільшення користувачів від 1 до безскінченності
    name = "users"
