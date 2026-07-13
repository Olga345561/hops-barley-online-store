from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Accounts: custom user model with email login."""

    default_auto_field = "django.db.models.BigAutoField" #BigAutoField збільшення продуктів від 1 до безскінченності
    name = "products"
