from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Question")
    answer = models.TextField(verbose_name="Respond")
    order = models.PositiveIntegerField(default=0, verbose_name="Sort order")

    class Meta:
        ordering = ['order']
        verbose_name = "Frequently asked question"
        verbose_name_plural = "Frequently asked questions (FAQ)"

    def __str__(self):
        return self.question