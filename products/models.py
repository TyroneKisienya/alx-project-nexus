from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,  decimal_places=2, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['price']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_PENDING = "Pending"
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  =models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"])
        ]

    def __str__(self):
        return f"order #{self.id} by {self.user.username}"

    def calculate(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"