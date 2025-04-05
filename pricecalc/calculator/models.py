from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание')
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Базовая цена'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

class PriceModifier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_modifiers')
    name = models.CharField(max_length=100, verbose_name='Название модификатора')
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Корректировка цены'
    )
    is_percentage = models.BooleanField(default=False, verbose_name='Процентная корректировка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Модификатор цены'
        verbose_name_plural = 'Модификаторы цен'

    def __str__(self):
        return f"{self.name} для {self.product.name}"

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решен'),
        ('closed', 'Закрыт'),
    ]

    session_id = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.email})"

    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'

class SupportMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    is_staff = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Сотрудник' if self.is_staff else 'Клиент'}: {self.message[:50]}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']
