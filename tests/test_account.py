import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from orders.models import Order

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="me@example.com", password="pass-123456", first_name="Ivan"
    )


def _order(user, status: str) -> Order:
    return Order.objects.create(
        user=user, status=status, full_name="I", phone="1", city="K", address="a"
    )


@pytest.mark.django_db
class TestAccount:
    def test_requires_login(self, client) -> None:
        response = client.get(reverse("users:account"))
        assert response.status_code == 302 and "login" in response.url

    def test_shows_own_orders_only(self, client, user) -> None:
        other = User.objects.create_user(email="other@example.com", password="x-123456")
        mine = _order(user, Order.Status.PENDING)
        theirs = _order(other, Order.Status.PENDING)
        client.force_login(user)
        html = client.get(reverse("users:account")).content.decode()
        assert f"#{mine.pk}" in html and f"#{theirs.pk}" not in html

    def test_filter_by_status(self, client, user) -> None:
        pending = _order(user, Order.Status.PENDING)
        delivered = _order(user, Order.Status.DELIVERED)
        client.force_login(user)
        html = client.get(reverse("users:account"), {"status": "delivered"}).content.decode()
        assert f"#{delivered.pk}" in html and f"#{pending.pk}" not in html

    def test_update_profile(self, client, user) -> None:
        client.force_login(user)
        client.post(
            reverse("users:account"),
            {"full_name": "Ivan Brewer", "email": "me@example.com",
             "phone": "+3805", "city": "Lviv", "address": "Rynok 1"},
        )
        user.refresh_from_db()
        assert user.last_name == "Brewer" and user.city == "Lviv"

    def test_change_password(self, client, user) -> None:
        client.force_login(user)
        response = client.post(
            reverse("users:password_change"),
            {"old_password": "pass-123456",
             "new_password1": "brand-new-pass-9", "new_password2": "brand-new-pass-9"},
        )
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.check_password("brand-new-pass-9")