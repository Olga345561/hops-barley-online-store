from django.urls import path
from .views import RecipeListView, RecipeDetailView

app_name = "guides_and_recipes"

urlpatterns = [
    path('guides/', RecipeListView.as_view(), name='recipe_list'),
    path('guides/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),

]