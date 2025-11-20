from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all(). order_by("id")
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    #sort
    ordering_fields = ['price', 'name', 'created_at']

    # search
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Product.objects.all().order_by("id")

        # category filter
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id = category_id)
        
        return queryset