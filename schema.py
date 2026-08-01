import graphene
from django.db.models import Sum, Avg, Count, F
from graphene_django import DjangoObjectType

from orders.models import Order
from products.models import Product
from users.models import User

# 1. Створюємо тип продуктів
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")

# 2. Створюємо тип замовлень
class OrderType(DjangoObjectType):
    total_quantity = graphene.Int()  # Загальна кількість товарів у замовленні

    class Meta:
        model = Order
        fields = ("id", "created_at", "total_price", "status", "user", "total_quantity")

    def resolve_total_quantity(self, info):
        return sum(item.quantity for item in self.items.all())

# 3. Створюємо тип користувача
class UserType(DjangoObjectType):
    orders_count = graphene.Int()
    is_repeat_customer = graphene.Boolean()

    class Meta:
        model = User
        fields = ("id", "email", "is_active", "date_joined")

    def resolve_orders_count(self, info):
        return self.orders.count()

    def resolve_is_repeat_customer(self, info):
        return self.orders.count() > 1


class Query(graphene.ObjectType):
    # --- Продукти ---
    all_products = graphene.List(ProductType)
    popular_products = graphene.List(ProductType)

    # --- Замовлення (Аналітика) ---
    total_revenue = graphene.Float()
    average_order_value = graphene.Float()
    orders_count = graphene.Int()

    # --- Користувачі (Аналітика) ---
    all_users = graphene.List(UserType)
    repeat_customers_count = graphene.Int()

    # Резолвери для продуктів
    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_popular_products(root, info):
        return Product.objects.order_by("-stock")[:5]

    # Резолвери для замовлень
    def resolve_total_revenue(root, info):
        result = Order.objects.aggregate(total=Sum("total_price"))
        return result["total"] if result["total"] is not None else 0.0

    def resolve_average_order_value(root, info):
        result = Order.objects.aggregate(avg_value=Avg("total_price"))["avg_value"]
        return result if result is not None else 0.0

    def resolve_orders_count(root, info):
        return Order.objects.count()

    # Резолвери для користувачів
    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_repeat_customers_count(root, info):
        return User.objects.annotate(num_orders=Count('orders')).filter(num_orders__gt=1).count()

schema = graphene.Schema(query=Query)