from django.shortcuts import render
# Убираем импорт моделей из catalog, так как они больше не нужны на главной

def index(request):
    # Убираем запросы к базе данных товаров
    # Просто рендерим главную страницу без товаров
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')