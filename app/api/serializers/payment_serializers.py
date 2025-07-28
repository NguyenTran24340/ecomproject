

from rest_framework import serializers
from app.models import CartOrder

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields = ['id', 'price', 'paid_status', 'order_date', 'product_status']
