from django.contrib import admin
from .models import ContactMessage  # Замініть ContactMessage на назву вашої моделі, якщо вона інша


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Поля, які будуть відображатися у вигляді таблиці списку
    list_display = ('id', 'name', 'email', 'created_at')

    # Поля, за якими можна клікнути, щоб перейти до редагування запису
    list_display_links = ('id', 'name')

    # Поля, за якими можна здійснювати пошук в адмінці
    search_fields = ('name', 'email', 'message')

    # Фільтри праворуч у списку (наприклад, за датою створення)
    list_filter = ('created_at',)