from django.urls import path
from .views import resources_view

app_name = 'resources'

urlpatterns = [
    path('resources/', resources_view, name='resources'),
]