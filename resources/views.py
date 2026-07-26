from django.shortcuts import render
from .models import Resource, ResourceCategory


def resources_view(request):
    # Отримуємо ресурси, відсортовані за категоріями
    calculators = Resource.objects.filter(category=ResourceCategory.CALCULATOR)
    guides = Resource.objects.filter(category=ResourceCategory.GUIDE)
    glossary = Resource.objects.filter(category=ResourceCategory.GLOSSARY)

    context = {
        'calculators': calculators,
        'guides': guides,
        'glossary': glossary,
    }

    return render(request, 'pages/resources.html', context)