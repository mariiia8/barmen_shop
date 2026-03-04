from django.db import models
from django.urls import reverse

class Category(models.Model):
    CATEGORY_TYPES = [
        ('course', 'Курс'),
        ('equipment', 'Оборудование'),
        ('book', 'Книга'),
    ]
    
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    type = models.CharField('Тип', max_length=20, choices=CATEGORY_TYPES)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField('В наличии', default=0)
    is_available = models.BooleanField('Доступен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    # Для курсов
    duration = models.CharField('Длительность курса', max_length=100, blank=True, help_text='Например: "3 месяца"')
    level = models.CharField('Уровень', max_length=50, blank=True, choices=[
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ])
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])

class OrderItem(models.Model):
    order = models.ForeignKey('crm.Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"