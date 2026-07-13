from django.http import HttpResponse
from django.urls import path

app_name = 'products'

def _placeholder (request, slug):
    return HttpResponse(status=204)

urlpatterns = [
    path('product/<slug:slug>/',_placeholder,name='detail'),
]
