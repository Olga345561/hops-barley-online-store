import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestOrderAPI:

    def setup_method(self):
        self.client = APIClient()
        # Створюємо тестового користувача
        self.user = User.objects.create_user(email="test@example.com", password="securepassword123")
        self.orders_url = reverse('api-orders-list')

    def test_get_orders_unauthorized(self):
        """Перевіряє, що неавторизований користувач не може отримати список замовлень"""
        response = self.client.get(self.orders_url)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_get_orders_authorized(self):
        """Перевіряє, що авторизований користувач може отримати список замовлень"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.orders_url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_order_unauthorized(self):
        """Перевіряє, що неавторизований користувач не може створити замовлення"""
        data = {
            "full_name": "Lanetska Olga",
            "phone": "01234567891",
            "city": "Odesa",
            "address": "str. Pushkina 15",
            "payment_method": "Debit Card"
        }
        response = self.client.post(self.orders_url, data, format='json')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_order_authorized(self):
        """Перевіряє, що авторизований користувач може успішно створити замовлення"""
        self.client.force_authenticate(user=self.user)
        data = {
            "full_name": "Lanetska Olga",
            "phone": "01234567891",
            "city": "Odesa",
            "address": "str. Pushkina 15",
            "payment_method": "Debit Card"
        }
        response = self.client.post(self.orders_url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED