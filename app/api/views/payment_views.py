from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from app.models import CartOrder
from app.api.serializers.payment_serializers import PaymentHistorySerializer

class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.session.get("order_id")
        if not order_id:
            return Response({"error": "No order ID found in session."}, status=400)

        try:
            order = CartOrder.objects.get(id=order_id, user=request.user)
        except CartOrder.DoesNotExist:
            return Response({"error": "Order not found."}, status=404)

        amount = float(order.price)
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': "%.2f" % amount,
            'item_name': f"Order-Item-No-{order.id}",
            'invoice': f"INVOICE_NO-{order.id}",
            'currency_code': "USD",
            'notify_url': f"http://{host}{reverse('app:paypal-ipn')}",
            'return_url': f"http://{host}{reverse('app:payment-completed')}",
            'cancel_url': f"http://{host}{reverse('app:payment-failed')}",
        }

        paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

        return Response({
            "form": paypal_payment_button.render()
        })


class PaymentHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="",
        responses={200: PaymentHistorySerializer(many=True)}
    )
    def get(self, request):
        orders = CartOrder.objects.filter(user=request.user, paid_status=True).order_by('-order_date')
        serializer = PaymentHistorySerializer(orders, many=True)
        return Response(serializer.data)
