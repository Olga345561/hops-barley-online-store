"""Створення замовлення: основна бізнес-логіка оформлення замовлення."""

from typing import Any

from django.db import transaction

from products.models import Product
from users.models import User

from .cart import Cart
from .models import Order, OrderItem


class InsufficientStock(Exception):
    """У рядку кошика запитується більше одиниць товару, ніж є в наявності."""

    def __init__(self, product: Product, available: int) -> None:
        self.product = product
        self.available = available
        super().__init__(f"{product.name}: only {available} available")


@transaction.atomic
def create_order(user: User, cart: Cart, **shipping: Any) -> Order:
    """Створіть замовлення з кошика, заблокувавши рядки та зменшивши кількість товару в наявності.

    Оплата імітується: замовлення на картку/гаманець одразу позначаються як ОПЛАЧЕНІ,
    оплата готівкою залишається В ОЧІКУВАННІ. Збільшує кількість товарів у недоступному
    запасі (і скасовує назад), якщо будь-який рядок перевищує доступний запас.
    """
    order = Order.objects.create(user=user, **shipping)
    total = order.total_price
    for item in cart:
        product = Product.objects.select_for_update().get(pk=item.product.pk)
        if item.quantity > product.stock:
            raise InsufficientStock(product, product.stock)
        product.stock -= item.quantity
        product.save(update_fields=["stock"])
        OrderItem.objects.create(
            order=order, product=product, quantity=item.quantity, price=product.price
        )
        total += product.price * item.quantity

    if order.payment_method != Order.PaymentMethod.COD:
        order.status = Order.Status.PAID  # успішно проведено фіктивний платіж

    order.total_price = total
    order.save(update_fields=["total_price", "status"])
    return order