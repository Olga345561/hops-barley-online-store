from django.db import models
from products.models import Product


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, max_length=200, verbose_name="Slug")
    description = models.TextField(verbose_name="Short Description")
    content = models.TextField(verbose_name="Full Instructions / Content")

    # Зв'язок із конкретним товаром/набором для швидкого переходу до замовлення
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
        verbose_name="Associated Product / Kit"
    )

    image = models.ImageField(max_length=255, blank=True, null=True, verbose_name="Image Path")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"