from django.http import HttpResponse
from django.urls import path

from products.urls import app_name

app_name = "users"

def _placeholder(request, HttRequest) -> HttpResponse:
    return HttpResponse(status=204)

urlpatterns = [
    path('account/', _placeholder, name='account'),
    path('account/login', _placeholder, name='login'),
    path('account/logout', _placeholder, name='logout'),
    path('account/register', _placeholder, name='register'),
]