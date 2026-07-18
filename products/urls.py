from django.http import HttpResponse
from django.urls import path
from .views import ProductListView

app_name = 'products'

def _placeholder (request, slug):
    return HttpResponse(status=204)

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('products/', ProductListView.as_view (),name='list'),
    path('product/<slug:slug>/',_placeholder,name='detail'),

]
