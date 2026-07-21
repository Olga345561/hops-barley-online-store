from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

User = get_user_model()


REGISTER = reverse("api-register")
LOGIN = reverse("api-login")
REFRESH = reverse("api-refresh")


@pytest.mark.django_db
class TestUsersApi:

    def test_register(self, client) -> None:
        response = client.post(
            REGISTER, {"email": "api@example.com", "password": "strong-pass-123"}
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": User.objects.get().pk,
            "email": "api@example.com",
        }

    def test_register_weak_password_400(self, client) -> None:
        assert (
            client.post(
                REGISTER, {"email": "a@a.com", "password": "1"}
            ).status_code
            == 400
        )

    def test_login_returns_token_pair_and_refresh_works(self, client) -> None:
        User.objects.create_user(
            email="jwt@example.com", password="strong-pass-123"
        )
        tokens = client.post(
            LOGIN,
            {"email": "jwt@example.com", "password": "strong-pass-123"},
        ).json()

        assert "access" in tokens and "refresh" in tokens

        refreshed = client.post(REFRESH, {"refresh": tokens["refresh"]})
        assert refreshed.status_code == 200 and "access" in refreshed.json()

    def test_login_wrong_password_401(self, client) -> None:
        User.objects.create_user(
            email="jwt@example.com", password="strong-pass-123"
        )
        assert (
            client.post(
                LOGIN, {"email": "jwt@example.com", "password": "no"}
            ).status_code
            == 401
        )