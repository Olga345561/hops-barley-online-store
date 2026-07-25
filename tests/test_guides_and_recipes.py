from django.test import TestCase
from django.urls import reverse
from guides_and_recipes.models import Recipe
from products.models import Product, Category  # Додано імпорт Category


class RecipeModelAndViewsTest(TestCase):

    def setUp(self):
        # 1. Спочатку створюємо категорію, оскільки вона обов'язкова для Product
        self.category = Category.objects.create(
            name="Beer Kits",
            slug="beer-kits"
        )

        # 2. Створюємо тестовий продукт із прив'язкою до категорії
        self.product = Product.objects.create(
            name="West Coast IPA Kit",
            slug="west-coast-ipa-kit",
            category=self.category,
            price=550.00,
            description="All grains and hops for West Coast IPA"
        )

        # 3. Створюємо тестовий рецепт із посиланням на продукт та унікальним slug
        self.recipe = Recipe.objects.create(
            title="How to brew West Coast IPA",
            slug="how-to-brew-west-coast-ipa",
            content="Detailed instructions on brewing a classic West Coast IPA...",
            product=self.product
        )

    def test_recipe_model_str(self):
        """Перевіряємо текстове представлення моделі (__str__)"""
        self.assertEqual(str(self.recipe), "How to brew West Coast IPA")

    def test_recipe_list_view(self):
        """Перевіряємо, чи сторінка зі списком рецептів відкривається і використовує правильний шаблон"""
        url = reverse("guides_and_recipes:recipe_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи використовується шаблон pages/guides.html
        self.assertTemplateUsed(response, "pages/guides.html")
        # Перевіряємо наявність назви рецепта у списку
        self.assertContains(response, self.recipe.title)

    def test_recipe_detail_view(self):
        """Перевіряємо, чи сторінка детального перегляду рецепта відкривається і містить дані"""
        url = reverse("guides_and_recipes:recipe_detail", kwargs={"slug": self.recipe.slug})
        response = self.client.get(url)

        # Перевіряємо успішність запиту
        self.assertEqual(response.status_code, 200)

        # Перевіряємо, чи на сторінці виводиться назва рецепта та контент
        self.assertContains(response, "How to brew West Coast IPA")
        self.assertContains(response, self.recipe.content)

        # Перевіряємо ціну пов'язаного набору, якщо вона виводиться
        self.assertContains(response, str(int(self.product.price)))