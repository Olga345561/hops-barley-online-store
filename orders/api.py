from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API-ендпоінт, який дозволяє переглядати, створювати та керувати замовленнями.
    Доступно лише авторизованим користувачам.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Звичайний користувач бачить лише свої замовлення, а адміністратор — усі
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        # Автоматично прив'язуємо замовлення до поточного залогіненого користувача
        serializer.save(user=self.request.user)

