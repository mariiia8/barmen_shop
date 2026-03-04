from django.contrib import admin
from .models import Client, Order
from catalog.models import OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Контактная информация', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Статус', {
            'fields': ('status', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'total_amount', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['client__name', 'client__phone']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline]