from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Каталог: категорії, товари, відгуки."""

    default_auto_field = "django.db.models.BigAutoField" #BigAutoField збільшення продуктів від 1 до безкінченності
    name = "products"
