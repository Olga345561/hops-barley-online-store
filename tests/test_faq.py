from django.test import TestCase
from django.urls import reverse


class FAQPageTests(TestCase):

    def test_faq_page_status_code(self):
        """Перевіряє, чи сторінка FAQ доступна (статус 200)"""
        response = self.client.get(reverse('faq:faq'))
        self.assertEqual(response.status_code, 200)

    def test_faq_page_template(self):
        """Перевіряє, чи використовується правильний шаблон для сторінки FAQ"""
        response = self.client.get(reverse('faq:faq'))
        self.assertTemplateUsed(response, 'pages/faq.html')

    def test_faq_page_contains_header_and_content(self):
        """Перевіряє наявність заголовка та загальної структури сторінки FAQ"""
        response = self.client.get(reverse('faq:faq'))

        # Перевірка заголовка сторінки, який реально є у виводі
        self.assertContains(response, "Frequently Asked Questions (FAQ)")
        self.assertContains(response, "Find answers to the most common questions")

        # Перевірка того стану, який зараз повертає шаблон (немає питань або є)
        # Якщо питань у базі немає, шаблон показує це повідомлення:
        self.assertContains(response, "No questions available at the moment.")