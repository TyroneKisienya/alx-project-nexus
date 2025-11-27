from django.urls import path
from .views import InitializePaymentView, chapa_webhook

urlpatterns = [
    path("init/<int:order_id>/", InitializePaymentView.as_view()),
    path("webhook/", chapa_webhook),
]
