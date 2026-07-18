"""Перегляди каталогу: список товарів з пошуком, фільтрацією, сортуванням, нумерацією сторінок."""

from decimal import Decimal, InvalidOperation
from typing import Any

from django.db.models import Avg, Count, F, Q, QuerySet
from django.views.generic import ListView

from .models import Category, Product

#: Зіставляє параметр GET `sort` з упорядкуванням ORM.
SORTS = {
    "new": "-created_at",
    "price_asc": "price",
    "price_desc": "-price",
}


class ProductListView(ListView):
    """Головна сторінка та `/products/`: каталог товарів з можливістю фільтрації."""

    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self) -> QuerySet[Product]:
        qs = (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .annotate(avg_rating=Avg("reviews__rating"), sold=Count("order_items"))
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        categories = self.request.GET.getlist("category")
        if categories:
            qs = qs.filter(category__slug__in=categories)

        qs = self._filter_price(qs)

        sort = self.request.GET.get("sort", "new")
        if sort == "rating":
            return qs.order_by(F("avg_rating").desc(nulls_last=True))
        if sort == "popular":
            return qs.order_by("-sold", "-created_at")
        return qs.order_by(SORTS.get(sort, "-created_at"))

    def _filter_price(self, qs: QuerySet[Product]) -> QuerySet[Product]:
        """Застосовуються межі price_min / price_max, ігноруючи неправильно сформовані вхідні дані."""
        for param, lookup in (("price_min", "price__gte"), ("price_max", "price__lte")):
            raw = self.request.GET.get(param, "").strip()
            if not raw:
                continue
            try:
                qs = qs.filter(**{lookup: Decimal(raw)})
            except InvalidOperation:
                continue
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_categories"] = self.request.GET.getlist("category")
        context["current_sort"] = self.request.GET.get("sort", "new")
        return context