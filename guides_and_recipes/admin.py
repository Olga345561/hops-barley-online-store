from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "product", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}