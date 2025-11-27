from django.shortcuts import render
from rest_framework import viewsets, filters, permissions 
from .models import Category, Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, OrderItemSerializer, OrderSerializer, CheckoutSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction
from decimal import Decimal
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


# Create your views here.

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #filter
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
    
class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    ordering_fields = ['created_at']

    search_fields = ['status', 'user__username']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=["post"], permission_classes = [permissions.IsAuthenticated])
    @transaction.atomic
    def checkout(self, request):
        serializer = CheckoutSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        items = serializer.validated_data["items"]
        order = Order.objects.create(
            user = request.user,
            status = Order.STATUS_PENDING,
            total_amount = 0,
        )

        total = Decimal("0.00")
        for item in items:
            product = Product.objects.select_for_update().get(id=item["product_id"])
            quantity = item["quantity"]
            price = product.price * quantity

            OrderItem.objects.create(
                order = order,
                product = product,
                quantity = quantity,
                price = product.price,
            )

            total += price

            order.total_amount = total
            order.save()

        return Response(
            {
                "message": "order created successfully",
                "order_id": order.id,
                "total": total,
                "status": order.status,
            },
            status = HTTP_201_CREATED
        )

    
class OrderItemviewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('order')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]

    search_fields = ['product__name']

    def get_queryset(self):
        queryset = OrderItem.objects.all(). order_by('order')

        order_id = self.request.query_params.get('order')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        return queryset