from rest_framework.routers import DefaultRouter
from .views import CategoryViewset, ProductViewset, OrderItemviewset, OrderViewset

router = DefaultRouter()

router.register(r'categories', CategoryViewset, basename='categories')
router.register(r'products', ProductViewset, basename='products')
router.register(r'orders', OrderViewset, basename='orders')
router.register(r'items', OrderItemviewset, basename='items')

urlpatterns = router.urls