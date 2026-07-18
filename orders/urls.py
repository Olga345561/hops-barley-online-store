from django.http import HttpResponse
from django.urls import path

from products.urls import app_name

app_name = "orders"

def _placeholder(request, HttRequest):
    return HttpResponse(status=204)

def _placeholder_pk(request, HttRequest):
    return HttpResponse(status=204)

urlpatterns = [
    path('cart/', _placeholder, name='cart'),
    path('cart/add/<int:product_id>/', _placeholder, name='cart_add'),
]