"""Checkout form styled with the design's classes."""

from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    """Інформація про доставку + спосіб оплати замовлення."""

    class Meta:
        model = Order
        fields = ["full_name", "phone", "city", "address", "payment_method"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "Input", "placeholder": "Value"}),
            "phone": forms.TextInput(attrs={"class": "Input", "placeholder": "Value"}),
            "city": forms.TextInput(attrs={"class": "Input", "placeholder": "Value"}),
            "address": forms.Textarea(
                attrs={"class": "Textarea", "rows": 3, "placeholder": "Value"}
            ),
            "payment_method": forms.RadioSelect(),
        }