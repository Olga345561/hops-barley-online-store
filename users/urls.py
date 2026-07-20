from django.http import HttpResponse
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from products.urls import app_name

app_name = "users"

def _placeholder(request, HttRequest) -> HttpResponse:
    return HttpResponse(status=204)

urlpatterns = [
    path('account/', _placeholder, name='account'),
    path('account/register', views.register, name='register'),
    path('account/login',views.UserLoginView.as_view(), name='login'),
    path('account/logout',auth_views.LogoutView.as_view(), name='logout'),
]

