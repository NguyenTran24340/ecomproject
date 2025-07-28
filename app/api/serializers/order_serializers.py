from rest_framework import serializers
from app.models import CartOrder, CartOrderItems

class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItems
        fields = ['invoice_no', 'item', 'image', 'qty', 'price', 'total', 'product_status']

class CartOrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CartOrder
        fields = ['id', 'price', 'paid_status', 'order_date', 'product_status', 'items']

    def get_items(self, obj):
        items = CartOrderItems.objects.filter(order=obj)
        return CartOrderItemSerializer(items, many=True).data
