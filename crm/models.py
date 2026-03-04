from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидание звонка'),
        ('contacted', 'Информация получена'),
        ('rejected', 'Отклонен'),
        ('purchased', 'Куплено'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20, unique=True)
    email = models.EmailField('Email', blank=True, null=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    notes = models.TextField('Заметки', blank=True)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone}"

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)
    is_completed = models.BooleanField('Завершен', default=False)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.client.name}"