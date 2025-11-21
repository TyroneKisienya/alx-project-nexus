from rest_framework.routers import DefaultRouter
from .views import CategoryViewset, ProductViewset

router = DefaultRouter()

router.register(r'categories', CategoryViewset, basename='categories')
router.register(r'products', ProductViewset, basename='products')

urlpatterns = router.urls