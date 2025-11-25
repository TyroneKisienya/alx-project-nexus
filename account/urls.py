from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, ProfileViewset, LogoutViewset, EmailVerificationViewset, PasswordResetViewset

router = DefaultRouter()
router.register(r'register', RegisterViewset, basename='auth-register')
router.register(r'me', ProfileViewset, basename='auth-me')
router.register(r'logout', LogoutViewset, basename="auth-logout")
router.register(r'verify-email', EmailVerificationViewset, basename="verify-email")
router.register(r"password-reset", PasswordResetViewset, basename="password-reset")
urlpatterns = [
    path("", include(router.urls))
]