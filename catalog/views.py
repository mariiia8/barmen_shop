from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
from crm.models import Client, Order
from django.contrib import messages

def product_list(request):
    category_slug = request.GET.get('category')
    product_type = request.GET.get('type')
    search_query = request.GET.get('search')
    
    products = Product.objects.filter(is_available=True)
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if product_type:
        products = products.filter(category__type=product_type)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_type': product_type,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)

def quick_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        product_id = request.POST.get('product_id')
        
        client, created = Client.objects.get_or_create(
            phone=phone,
            defaults={'name': name, 'status': 'waiting'}
        )
        
        if not created:
            client.name = name
            client.save()
        
        messages.success(request, 'Спасибо! Мы скоро свяжемся с вами.')
        return render(request, 'catalog/order_success.html')
    
    return render(request, 'catalog/quick_order.html')