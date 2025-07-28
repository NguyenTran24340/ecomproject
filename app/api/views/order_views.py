from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from app.models import CartOrder, CartOrderItems
from app.api.serializers.order_serializers import CartOrderSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="")
    def post(self, request):
        cart_data = request.session.get('cart_data_obj', {})
        if not cart_data:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = CartOrder.objects.create(user=request.user, price=0)
        total_price = 0
        for item in cart_data.values():
            price = float(item['price'].replace('$', ''))
            total = price * int(item['qty'])
            CartOrderItems.objects.create(
                order=order,
                invoice_no="INV-" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=price,
                total=total,
                product_status="processing"
            )
            total_price += total

        order.price = total_price
        order.save()

        # Clear session cart
        request.session.pop('cart_data_obj', None)

        return Response({"order_id": order.id, "total": total_price}, status=status.HTTP_201_CREATED)

class OrderHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="")
    def get(self, request):
        orders = CartOrder.objects.filter(user=request.user).order_by("-id")
        serializer = CartOrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="")
    def get(self, request, id):
        try:
            order = CartOrder.objects.get(user=request.user, id=id)
        except CartOrder.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        serializer = CartOrderSerializer(order)
        return Response(serializer.data)

class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="")
    def get(self, request, id):
        try:
            order = CartOrder.objects.get(user=request.user, id=id)
        except CartOrder.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        serializer = CartOrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="")
    def delete(self, request, id):
        try:
            order = CartOrder.objects.get(user=request.user, id=id)
        except CartOrder.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        order.delete()
        return Response({"detail": "Order deleted successfully"}, status=204)
