from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum, Avg, Count
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "payment_method", "total_price", "created_at")
    list_filter = ("status", "payment_method")
    inlines = [OrderItemInline]

    # 1. Додаємо кастомний шлях в URL адмінки для сторінки аналітики
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('store-analytics/', self.admin_site.admin_view(self.analytics_view), name="store_analytics"),
        ]
        return custom_urls + urls

    # 2. Логіка збору даних (повністю дублює те, що рахує schema.py)
    def analytics_view(self, request):
        # Замовлення та фінанси
        total_revenue = Order.objects.aggregate(total=Sum("total_price"))["total"] or 0.0
        average_order_value = Order.objects.aggregate(avg=Avg("total_price"))["avg"] or 0.0
        orders_count = Order.objects.count()

        # Продукти (популярні товари за залишком, як у схемі)
        popular_products = Product.objects.order_by("-stock")[:5]

        # Користувачі та повторні покупці
        all_users_count = User.objects.count()
        repeat_customers_count = User.objects.annotate(num_orders=Count('orders')).filter(num_orders__gt=1).count()

        context = {
            **self.admin_site.each_context(request),
            "title": "Аналітика інтернет-магазину",
            "total_revenue": total_revenue,
            "average_order_value": average_order_value,
            "orders_count": orders_count,
            "popular_products": popular_products,
            "all_users_count": all_users_count,
            "repeat_customers_count": repeat_customers_count,
        }

        return TemplateResponse(request, "admin/orders/analytics.html", context)