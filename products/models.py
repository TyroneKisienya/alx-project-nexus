from django.db import models

# Create your models here.

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
