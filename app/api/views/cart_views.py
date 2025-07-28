from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.models import Product


from app.api.serializers.cart_serializers import (
    AddToCartSerializer,
    UpdateCartSerializer,
    RemoveFromCartSerializer,
)

class CartView(APIView):
    def get(self, request):
        cart = request.session.get('cart_data_obj', {})
        return Response(cart)

class AddToCartView(APIView):
    @swagger_auto_schema(request_body=AddToCartSerializer)
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            product_id = data['pid']

            cart = request.session.get('cart_data_obj', {})
            if product_id in cart:
                cart[product_id]['qty'] += int(data['qty'])
            else:
                cart[product_id] = {
                    'title': data['title'],
                    'qty': int(data['qty']),
                    'price': data['price'],
                    'image': data['image'],
                    'pid': data['pid'],
                }

            request.session['cart_data_obj'] = cart
            return Response({"message": "Added to cart", "cart": cart}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateCartView(APIView):
    @swagger_auto_schema(request_body=UpdateCartSerializer)
    def put(self, request):
        serializer = UpdateCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            product_qty = serializer.validated_data['product_qty']

            cart = request.session.get('cart_data_obj', {})
            if product_id in cart:
                cart[product_id]['qty'] = product_qty
                request.session['cart_data_obj'] = cart
                return Response({"message": "Cart updated", "cart": cart})
            return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartView(APIView):
    @swagger_auto_schema(request_body=RemoveFromCartSerializer)
    def delete(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            cart = request.session.get('cart_data_obj', {})
            if product_id in cart:
                del cart[product_id]
                request.session['cart_data_obj'] = cart
                return Response({"message": "Product removed from cart", "cart": cart})
            return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
