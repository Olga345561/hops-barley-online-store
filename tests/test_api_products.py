from decimal import Decimal
from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient

from orders.models import Order, OrderItem
from products.models import Category, Product

User = get_user_model()


@pytest.fixture
def api() -> APIClient:
    return APIClient()


@pytest.fixture
def catalog() -> dict:
    hops = Category.objects.create(name="Hops", slug="hops")
    malts = Category.objects.create(name="Malts", slug="malts")
    citra = Product.objects.create(
        name="Citra",
        slug="citra",
        description="Tropical",
        price=Decimal("5.99"),
        category=hops,
        stock=50
    )

    pilsner = Product.objects.create(
        name="Pilsner Malt",
        slug="pilsner-malt",
        description="Base malt",
        price=Decimal("3.50"),
        category=malts,
        stock=100
    )

    return {'citra': citra, 'pilsner': pilsner, 'malts': malts}


def _auth(api: APIClient, email: str = "a@example.com") -> "User":
    user = User.objects.create_user(email=email, password="admin-123456")
    tokens = api.post(
        path="/api/users/login/",
        data={"email": email, "password": "admin-123456"}
    ).json()
    # Для SimpleJWT зазвичай використовується "Bearer", а не "Token"
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    return user


@pytest.mark.django_db
class TestProductsApi:

    def test_list_paginated(self, api: APIClient, catalog: dict) -> None:
        data = api.get("/api/products/").json()
        assert data["count"] == 2 and len(data["results"]) == 2

    def test_filter_by_category_and_price(self, api: APIClient, catalog: dict) -> None:
        assert api.get(path="/api/products/", data={"category": "hops"}).json()["count"] == 1
        assert api.get(path="/api/products/", data={"price_max": "4"}).json()["count"] == 1

    def test_search_and_ordering(self, api: APIClient, catalog: dict) -> None:
        assert api.get(path="/api/products/", data={"search": "tropical"}).json()["count"] == 1
        results = api.get(path="/api/products/", data={"ordering": "price"}).json()["results"]
        assert results[0]["name"] == "Pilsner Malt"

    def test_detail(self, api: APIClient, catalog: dict) -> None:
        data = api.get(f"/api/products/{catalog['citra'].pk}/").json()
        assert data["name"] == "Citra" and "avg_rating" in data

    def test_review_requires_purchase(self, api: APIClient, catalog: dict) -> None:
        _auth(api)
        response = api.post(
            f"/api/products/{catalog['citra'].pk}/reviews/",
            data={"rating": 5, "comment": "Great product!"}
        )
        assert response.status_code in [400, 403]