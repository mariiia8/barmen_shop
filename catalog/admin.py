from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['type']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available']
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Для курсов', {
            'fields': ('duration', 'level'),
            'classes': ('collapse',)
        }),
    )