from rest_framework import serializers
from app.models import Coupon

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount', 'active']