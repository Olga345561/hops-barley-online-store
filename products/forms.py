"""Форми каталогу."""

from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """Зірковий рейтинг із коментарем; стилізований під класи форм дизайну."""

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[(i, f"{i} / 5") for i in range(5, 0, -1)],
                attrs={"class": "Input"},
            ),
            "comment": forms.Textarea(attrs={"class": "Textarea", "rows": 3}),
        }