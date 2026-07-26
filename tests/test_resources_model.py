from django.test import TestCase
from resources.models import Resource, ResourceCategory

class ResourceModelTest(TestCase):

    def setUp(self):
        # Створюємо базовий об'єкт для тестів
        self.resource = Resource.objects.create(
            title="ABV Calculator",
            category=ResourceCategory.CALCULATOR,
            description="Calculate alcohol by volume."
        )

    def test_resource_creation(self):
        # Перевіряємо, чи об'єкт успішно створився і зберіг поля
        self.assertEqual(self.resource.title, "ABV Calculator")
        self.assertEqual(self.resource.category, ResourceCategory.CALCULATOR)
        self.assertEqual(self.resource.description, "Calculate alcohol by volume.")

    def test_slug_generation(self):
        # Перевіряємо, чи автоматично згенерувався slug
        self.assertEqual(self.resource.slug, "abv-calculator")

    def test_str_representation(self):
        # Перевіряємо метод __str__
        expected_str = "[Calculator] ABV Calculator"
        self.assertEqual(str(self.resource), expected_str)