"""Правила ведення каталогу."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from orders.models import Order
from users.models import User

from .models import Product


def user_has_purchased(user: AbstractBaseUser | AnonymousUser, product: Product) -> bool:
    """Істина, якщо користувач має оплачене/відправлене/доставлене замовлення, що містить товар."""
    if not isinstance(user, User):
        return False
    return Order.objects.filter(
        user=user, status__in=Order.PAID_STATUSES, items__product=product
    ).exists()