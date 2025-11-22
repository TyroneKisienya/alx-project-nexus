from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, ProfileViewset

router = DefaultRouter()
router.register(r'register', RegisterViewset, basename='auth-register')
router.register(r'me', ProfileViewset, basename='auth-me')

urlpatterns = [
    path("", include(router.urls))
]