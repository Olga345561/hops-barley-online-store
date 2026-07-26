from django.urls import path
from .views import community_list, create_community_post

app_name = 'community'

urlpatterns = [
    path('community/', community_list, name='community_list'),
    path('community/create/', create_community_post, name='community_create_post'),

]



