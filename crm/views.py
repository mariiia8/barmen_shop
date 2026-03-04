from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Client, Order
from catalog.models import OrderItem, Product
from django.db.models import Q

@staff_member_required
def crm_dashboard(request):
    total_clients = Client.objects.count()
    new_clients = Client.objects.filter(status='waiting').count()
    total_orders = Order.objects.count()
    
    recent_clients = Client.objects.order_by('-created_at')[:10]
    recent_orders = Order.objects.order_by('-created_at')[:10]
    
    context = {
        'total_clients': total_clients,
        'new_clients': new_clients,
        'total_orders': total_orders,
        'recent_clients': recent_clients,
        'recent_orders': recent_orders,
    }
    return render(request, 'crm/dashboard.html', context)

@staff_member_required
def client_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    clients = Client.objects.all()
    
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) | 
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if status_filter:
        clients = clients.filter(status=status_filter)
    
    context = {
        'clients': clients,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Client.STATUS_CHOICES,
    }
    return render(request, 'crm/client_list.html', context)

@staff_member_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    orders = client.orders.all()
    
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.phone = request.POST.get('phone')
        client.email = request.POST.get('email')
        client.status = request.POST.get('status')
        client.notes = request.POST.get('notes')
        client.save()
        messages.success(request, 'Информация о клиенте обновлена')
        return redirect('crm:client_detail', client_id=client.id)
    
    context = {
        'client': client,
        'orders': orders,
        'status_choices': Client.STATUS_CHOICES,
    }
    return render(request, 'crm/client_detail.html', context)

@staff_member_required
def create_order(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        product_ids = request.POST.getlist('products')
        
        client = get_object_or_404(Client, id=client_id)
        order = Order.objects.create(client=client, total_amount=0)
        
        total = 0
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            quantity = int(request.POST.get(f'quantity_{product_id}', 1))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            total += product.price * quantity
        
        order.total_amount = total
        order.save()
        
        messages.success(request, 'Заказ создан успешно')
        return redirect('crm:client_detail', client_id=client.id)
    
    clients = Client.objects.all()
    products = Product.objects.filter(is_available=True)
    
    context = {
        'clients': clients,
        'products': products,
    }
    return render(request, 'crm/create_order.html', context)