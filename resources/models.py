from django.db import models
from django.utils.text import slugify


class ResourceCategory(models.TextChoices):
    CALCULATOR = 'calculator', 'Calculator'
    GUIDE = 'guide', 'Step-by-step guide'
    GLOSSARY = 'glossary', 'Glossary of terms'



class Resource(models.Model):
    title = models.CharField(max_length=255, verbose_name="Resource name")
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    category = models.CharField(
        max_length=20,
        choices=ResourceCategory.choices,
        default=ResourceCategory.GUIDE,
        verbose_name="Category"
    )
    description = models.TextField(blank=True, verbose_name="Short description")
    content = models.TextField(blank=True, verbose_name="Full text / HTML / Instruction")

    # Поля для калькуляторів або файлів (якщо потрібно прикріпити інструкцію-PDF чи формулу)
    external_url = models.URLField(blank=True, null=True, verbose_name="Link to external tool/calculator")
    file = models.FileField(upload_to='resources/files/', blank=True, null=True, verbose_name="File (e.g. PDF)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated")

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        ordering = ['category', 'title']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)