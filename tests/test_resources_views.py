from django.test import TestCase
from django.urls import reverse
from resources.models import Resource, ResourceCategory

class ResourcesViewsTest(TestCase):

    def setUp(self):
        # Створюємо тестові дані для перевірки виведення на сторінці
        self.calculator_resource = Resource.objects.create(
            title="ABV Calculator",
            category=ResourceCategory.CALCULATOR,
            description="Calculate alcohol by volume."
        )
        self.guide_resource = Resource.objects.create(
            title="Sanitization Guide",
            category=ResourceCategory.GUIDE,
            description="How to clean equipment."
        )
        self.glossary_resource = Resource.objects.create(
            title="IBU",
            category=ResourceCategory.GLOSSARY,
            description="International Bitterness Units."
        )

    def test_resources_page_status_and_template(self):
        # Перевіряємо статус і шаблон
        response = self.client.get(reverse('resources:resources'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/resources.html')

    def test_resources_in_context(self):
        # Перевіряємо, чи дані приходять у контекст
        response = self.client.get(reverse('resources:resources'))
        self.assertIn('calculators', response.context)
        self.assertIn('guides', response.context)
        self.assertIn('glossary', response.context)

        self.assertIn(self.calculator_resource, response.context['calculators'])
        self.assertIn(self.guide_resource, response.context['guides'])
        self.assertIn(self.glossary_resource, response.context['glossary'])