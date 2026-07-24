from django.db import models
from django.conf import settings


class ContactMessage(models.Model):
    # Якщо користувач залогінений, прив'язуємо до нього. Якщо гість — залишаємо порожнім (NULL)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Користувач"
    )

    # Для незалогінених гостей залишаємо поля введення вручну
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")

    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Response date")
    is_processed = models.BooleanField(default=False, verbose_name="Processed")

    def __str__(self):
        author = self.user.email if self.user else f"{self.name} (Guest)"
        return f"Message from {author} — {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Contact message"
        verbose_name_plural = "Contact notifications"
        ordering = ['-created_at']