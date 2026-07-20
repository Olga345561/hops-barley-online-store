"""Перегляди облікового запису: реєстрація, вхід, сторінка облікового запису, зміна пароля."""

from typing import Any, cast

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from orders.models import Order

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User


class UserLoginView(LoginView):
    """Вхід до сеансу за допомогою шаблону дизайну."""

    template_name = "users/login.html"
    authentication_form = LoginForm


def register(request: HttpRequest) -> HttpResponse:
    """Створіть обліковий запис і негайно увійдіть у систему користувача."""
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        if not form.cleaned_data["remember_me"]:
            request.session.set_expiry(0)  # файл cookie сеансу браузера
        messages.success(request, "Welcome to Hop & Barley!")
        return redirect("products:home")
    return render(request, "users/register.html", {"form": form})


@login_required
def account(request: HttpRequest) -> HttpResponse:
    """Сторінка облікового запису: історія замовлень з фільтром статусу, редагування профілю."""
    user = cast(User, request.user)  # guaranteed by @login_required
    form = ProfileForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("users:account")

    orders = Order.objects.filter(user=user).prefetch_related("items")
    status = request.GET.get("status", "")
    if status in Order.Status.values:
        orders = orders.filter(status=status)
    page = Paginator(orders, 5).get_page(request.GET.get("page"))

    return render(
        request,
        "users/account.html",
        {
            "form": form,
            "orders_page": page,
            "current_status": status,
            "statuses": Order.Status.choices,
            "password_form": PasswordChangeForm(user=request.user),
        },
    )


class UserPasswordChangeView(PasswordChangeView):
    """POST-only password change from the account page tab."""

    success_url = reverse_lazy("users:account")
    template_name = "users/account.html"

    def form_valid(self, form: Any) -> HttpResponse:
        messages.success(self.request, "Password changed.")
        return super().form_valid(form)

    def form_invalid(self, form: Any) -> HttpResponse:
        for error in form.errors.values():
            messages.error(self.request, error.as_text())
        return redirect("users:account")