from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .models import Payment
from .services.chapa import initialize_payment
from products.models import Order

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class InitializePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        payment, created = Payment.objects.get_or_create(
            order=order,
            user=request.user,
            defaults={"amount": order.total_amount, "tx_ref": ""},
        )

        response, tx_ref = initialize_payment(
            amount=order.total_amount,
            email=request.user.email,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            callback_url="https://yourdomain.com/api/payments/verify/",
        )

        payment.tx_ref = tx_ref
        payment.save()

        return Response({
            "checkout_url": response["data"]["checkout_url"]
        }, status=HTTP_201_CREATED)
    
@csrf_exempt
@api_view(["POST"])
def chapa_webhook(request):
    tx_ref = request.data.get("tx_ref")

    payment = Payment.objects.get(tx_ref=tx_ref)
    payment.status = Payment.STATUS_SUCCESS
    payment.save()

    payment.order.status = "PAID"
    payment.order.save()

    return Response({"status": "ok"})
