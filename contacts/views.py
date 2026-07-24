from django.contrib import messages
from django.shortcuts import redirect, render
from .models import ContactMessage  # Імпортуємо нашу модель


def contact_view(request):
  if request.method == "POST":
    # Збираємо дані з полів форми (name, email, message відповідають атрибутам name="" в HTML)
    name = request.POST.get("name")
    email = request.POST.get("email")
    message_text = request.POST.get("message")

    # Базова перевірка, чи поля не порожні
    if not name or not email or not message_text:
      messages.error(request, "Please fill out all form fields.")
      return redirect("contact")  # Замініть 'contact' на назву вашого URL-шляху

    # Якщо користувач залогінений, беремо його об'єкт, інакше залишаємо None
    user = request.user if request.user.is_authenticated else None

    # Створюємо та зберігаємо повідомлення в базі даних
    ContactMessage.objects.create(
        user=user, name=name, email=email, message=message_text
    )

    # Виводимо повідомлення про успіх (воно автоматично з'явиться у вашому base.html завдяки блоку messages)
    messages.success(
        request, "Thank you! Your message has been sent successfully. We will contact you shortly."
    )
    return redirect("contact")

  return render(request, "contacts.html")