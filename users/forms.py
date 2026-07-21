"""Форми облікових записів, стилізовані під дизайн (електронна пошта + єдиний пароль)."""

from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from .models import User


class LoginForm(AuthenticationForm):
    """Вхід за допомогою електронної пошти/пароля з використанням вхідних класів дизайну."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "Input", "placeholder": "Value"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "Input", "placeholder": "Value"}
        )


class RegisterForm(forms.ModelForm):
    """Реєстрація точно так, як було задумано: електронна пошта, пароль, запам'ятати мене."""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "Input", "placeholder": "Value"})
    )
    remember_me = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={"class": "Input", "placeholder": "Value"})}

    def clean_password(self) -> str:
        password: str = self.cleaned_data["password"]
        validate_password(password)
        return password

    def save(self, commit: bool = True) -> User:
        """Створіть користувача з правильно хешованим паролем."""
        return User.objects.create_user(
            email=self.cleaned_data["email"], password=self.cleaned_data["password"]
        )

class ProfileForm(forms.ModelForm):
    """Особиста інформація на сторінці облікового запису; повне ім'я відповідає імені/прізвищу."""

    full_name = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={"class": "Input", "placeholder": "Value"}),
    )

    class Meta:
        model = User
        fields = ["email", "phone", "city", "address"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "Input"}),
            "phone": forms.TextInput(attrs={"class": "Input"}),
            "city": forms.TextInput(attrs={"class": "Input"}),
            "address": forms.Textarea(attrs={"class": "Textarea", "rows": 3}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["full_name"].initial = self.instance.get_full_name()

    def save(self, commit: bool = True) -> User:
        """Розділіть повне ім'я на ім'я/прізвище перед збереженням."""
        user: User = super().save(commit=False)
        first, _, last = self.cleaned_data.get("full_name", "").partition(" ")
        user.first_name, user.last_name = first, last
        if commit:
            user.save()
        return user


