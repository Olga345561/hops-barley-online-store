from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Замовлення та кошик."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
