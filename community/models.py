from django.db import models
from django.conf import settings


class CommunityPost(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    verbose_name="User"
    )
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Post Content")
    image = models.ImageField(upload_to="community/", blank=True, null=True, verbose_name="Photo")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.title} by {self.user.email}"

    class Meta:
        verbose_name = "Community Post"
        verbose_name_plural = "Community Posts"
        ordering = ["-created_at"]