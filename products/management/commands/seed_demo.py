"""Ідемпотентні демо-дані: продукти, демо-користувачі, замовлення, відгуки."""

from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from orders.models import Order
from products.models import Category, Product, Review

CATEGORIES = ["Hops", "Malts", "Yeast", "Adjuncts", "Kits"]

# (name, slug, category, price, stock, description) — опис на окремому рядку,
# щоб не перевищити ліміт flake8 у 100 символів на довгих назвах.
PRODUCTS = [
    ("Citra Hops", "citra-hops", "Hops", "5.99", 25,
     "Explosive citrus and tropical aroma, perfect for hazy IPAs."),
    ("Cascade Hops", "cascade-hops", "Hops", "7.49", 30,
     "The classic American aroma hop: floral and grapefruit."),
    ("Centennial Hops", "centennial-hops", "Hops", "6.49", 18,
     "A super-Cascade with intense floral and citrus character."),
    ("Mosaic Hops", "mosaic-hops", "Hops", "8.99", 12,
     "Complex blueberry, mango and pine layers."),
    ("Saaz Hops", "saaz-hops", "Hops", "5.49", 40,
     "Noble Czech hop with a delicate earthy, herbal aroma."),
    ("Caramel Malt", "caramel-malt", "Malts", "3.99", 50,
     "Toffee and caramel sweetness with a rich amber colour."),
    ("Maris Otter Malt", "maris-otter-malt", "Malts", "4.79", 35,
     "The legendary British base malt with a rich biscuit flavour."),
    ("Pilsner Malt", "pilsner-malt", "Malts", "3.49", 60,
     "Pale, clean and crisp continental base malt for lagers."),
    ("Imperial Yeast", "imperial-yeast", "Yeast", "12.99", 15,
     "Premium liquid yeast with high cell counts for fast starts."),
    ("Safale US-05 Yeast", "safale-us05-yeast", "Yeast", "4.99", 45,
     "The workhorse American ale strain: clean and forgiving."),
    ("Unmalted Wheat", "unmalted-wheat", "Adjuncts", "2.99", 55,
     "Raw wheat for witbiers and lambics; adds haze and body."),
    ("West Coast IPA Kit", "west-coast-ipa-kit", "Kits", "49.99", 8,
     "Everything for 20 litres of resinous, bitter West Coast IPA."),
]

REVIEWS = [
    ("citra-hops", 0, 5, "Absolute tropical bomb. My NEIPA has never smelled better."),
    ("cascade-hops", 1, 5, "Solid and dependable. The grapefruit note is perfect."),
    ("maris-otter-malt", 2, 5, "You can taste the difference in every English ale."),
    ("safale-us05-yeast", 0, 4, "Clean fermentation every single time."),
    ("west-coast-ipa-kit", 2, 5, "First brew ever and it came out fantastic."),
]


class Command(BaseCommand):
    """Seed the catalog with demo data (safe to re-run)."""

    help = "Create demo categories, products, users, orders and reviews."

    def handle(self, *args: Any, **options: Any) -> None:
        categories = {
            name: Category.objects.get_or_create(slug=name.lower(), defaults={"name": name})[0]
            for name in CATEGORIES
        }
        for name, slug, cat, price, stock, description in PRODUCTS:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name, "category": categories[cat], "price": Decimal(price),
                    "stock": stock, "description": description,
                },
            )
        users = self._seed_users()
        self._seed_orders_and_reviews(users)
        self.stdout.write(self.style.SUCCESS("Demo data ready."))

    def _seed_users(self) -> list[Any]:
        user_model = get_user_model()
        users = []
        for i in range(1, 4):
            email = f"demo{i}@hopandbarley.example"
            user = user_model.objects.filter(email=email).first()
            if user is None:
                user = user_model.objects.create_user(
                    email=email, password="demo-pass-123",
                    first_name=f"Demo{i}", last_name="Brewer",
                )
            users.append(user)
        if not user_model.objects.filter(email="admin@hopandbarley.example").exists():
            user_model.objects.create_superuser(
                email="admin@hopandbarley.example", password="admin"
            )
        return users

    def _seed_orders_and_reviews(self, users: list[Any]) -> None:
        if Order.objects.exists():
            return
        for user in users:
            Order.objects.create(
                user=user, status=Order.Status.DELIVERED,
                full_name=user.get_full_name(), phone="+380501112233",
                city="Kyiv", address="Khreshchatyk 1",
            )
        for slug, user_idx, rating, comment in REVIEWS:
            Review.objects.get_or_create(
                product=Product.objects.get(slug=slug), user=users[user_idx],
                defaults={"rating": rating, "comment": comment},
            )
