"""Перегляд кошика та оформлення замовлення."""
from typing import cast

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from products.models import Product
from users.models import User

from .cart import Cart, CartQuantityError
from .emails import send_order_emails
from .forms import CheckoutForm
from .models import Order
from .services import InsufficientStock, create_order

def cart_detail(request: HttpRequest) -> HttpResponse:
    """Відображати вміст кошика з загальними сумами, обчисленими сервером."""
    return render(request, "orders/cart.html", {"cart": Cart(request)})


def _quantity(request: HttpRequest) -> int:
    """Розберіть поле кількості, встановивши за замовчуванням значення 1."""
    try:
        return max(1, int(request.POST.get("quantity", "1")))
    except ValueError:
        return 1


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    """Додати N одиниць товару до кошика сесії."""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        Cart(request).add(product, _quantity(request))
        messages.success(request, f"{product.name} added to your cart.")
    except CartQuantityError as exc:
        messages.error(request, f"Only {exc.available} item(s) of {product.name} available.")
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect("orders:cart")


@require_POST
def cart_update(request: HttpRequest, product_id: int) -> HttpResponse:
    """Встановіть точну кількість для рядка кошика."""
    product = get_object_or_404(Product, pk=product_id)
    try:
        Cart(request).set_quantity(product, _quantity(request))
    except CartQuantityError as exc:
        messages.error(request, f"Only {exc.available} item(s) of {product.name} available.")
    return redirect("orders:cart")


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    """Видаліть лінійку товарів з кошика."""
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).remove(product)
    return redirect("orders:cart")

@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    """Сторінка оформлення замовлення: підтвердження форми, створення замовлення, надсилання електронних листів."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("orders:cart")

    user = cast(User, request.user)  # guaranteed by @login_required
    form = CheckoutForm(
        request.POST or None,
        initial={
            "full_name": user.get_full_name(), "phone": user.phone,
            "city": user.city, "address": user.address,
        },
    )
    if request.method == "POST" and form.is_valid():
        try:
            order = create_order(user, cart, **form.cleaned_data)
        except InsufficientStock as exc:
            messages.error(
                request,
                f"Only {exc.available} item(s) of {exc.product.name} available.",
            )
        else:
            cart.clear()
            send_order_emails(order)
            return redirect("orders:success", pk=order.pk)
    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def order_success(request: HttpRequest, pk: int) -> HttpResponse:
    """Сторінка подяки після успішного оформлення замовлення."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})