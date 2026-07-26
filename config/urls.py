"""
Конфігурація URL-адреси для проєкту config.

Список `urlpatterns` спрямовує URL-адреси до представлень. Для отримання додаткової інформації див.:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
Приклади:
Представлення функцій
1. Додати імпорт: from my_app import views
2. Додати URL-адресу до urlpatterns: path('', views.home, name='home')
Представлення на основі класів
1. Додати імпорт: from other_app.views import Home
2. Додати URL-адресу до urlpatterns: path('', Home.as_view(), name='home')
Включення іншої URLconf
1. Імпортувати функцію include(): from django.urls import include, path
2. Додати URL-адресу до urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from products.api import ProductViewSet
from users.api import RegisterAPIView

router = routers.DefaultRouter()
router.register('api/products', ProductViewSet, basename='api-products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
    path('', include('orders.urls')),
    path('', include('guides_and_recipes.urls')),
    path('', include('community.urls')),
    path('', include('contacts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

    path('api/users/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/users/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/users/refresh/', TokenRefreshView.as_view(), name='api-refresh'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)