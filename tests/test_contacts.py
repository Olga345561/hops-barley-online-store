from django.test import TestCase
from django.urls import reverse
from contacts.models import ContactMessage
from users.models import User

class ContactViewTests(TestCase):

  def setUp(self):
    # Створюємо тестового користувача на основі вашої кастомної моделі User (де логін — це email)
    self.user = User.objects.create_user(
        email="test@example.com", password="securepassword123"
    )
    # Припускаємо, що шлях у urls.py зареєстрований з name='contact'
    self.contact_url = reverse("contact")

  def test_contact_page_GET(self):
    """Тест: сторінка контактів успішно завантажується (статус 200)"""
    response = self.client.get(self.contact_url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "pages/contacts.html")

  def test_contact_form_success_guest(self):
    """Тест: успішне відправлення форми незалогіненим користувачем (гостем)"""
    form_data = {
        "name": "Іван Іванченко",
        "email": "ivan@example.com",
        "message": "Привіт! Хочу купити пиво оптом.",
    }
    response = self.client.post(self.contact_url, data=form_data)

    # Має відбутися редирект після успішного збереження
    self.assertRedirects(response, self.contact_url)

    # Перевіряємо, чи з'явився запис у базі даних
    self.assertEqual(ContactMessage.objects.count(), 1)
    message_obj = ContactMessage.objects.first()
    self.assertEqual(message_obj.name, "Іван Іванченко")
    self.assertEqual(message_obj.email, "ivan@example.com")
    self.assertIsNone(message_obj.user)  # Гость не повинен мати прив'язки до юзера

  def test_contact_form_success_authenticated_user(self):
    """Тест: успішне відправлення форми залогіненим користувачем"""
    # Логінимось під нашим тестовим користувачем
    self.client.login(email="test@example.com", password="securepassword123")

    form_data = {
        "name": "Authorized Customer",
        "email": "test@example.com",
        "message": "Questions about delivery.",
    }
    response = self.client.post(self.contact_url, data=form_data)

    self.assertRedirects(response, self.contact_url)

    # Перевіряємо базу даних
    self.assertEqual(ContactMessage.objects.count(), 1)
    message_obj = ContactMessage.objects.first()
    # Перевіряємо, чи автоматично підтягнувся поточний залогінений користувач
    self.assertEqual(message_obj.user, self.user)

  def test_contact_form_empty_fields(self):
    """Тест: відправка порожньої форми виводить помилку і не створює запис"""
    form_data = {"name": "", "email": "", "message": ""}
    response = self.client.post(self.contact_url, data=form_data)

    # Має перенаправити назад без збереження
    self.assertRedirects(response, self.contact_url)

    # Перевіряємо, що в базу нічого не записалося
    self.assertEqual(ContactMessage.objects.count(), 0)