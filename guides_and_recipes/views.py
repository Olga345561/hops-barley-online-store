from django.views.generic import DetailView, ListView
from .models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = "pages/guides.html"
    context_object_name = "recipes"

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "pages/recipe_detail.html"
    context_object_name = "recipe"