from rest_framework import serializers

class AddToCartSerializer(serializers.Serializer):
    title = serializers.CharField()
    qty = serializers.IntegerField()
    price = serializers.CharField()
    image = serializers.CharField()  
    pid = serializers.CharField()

class UpdateCartSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_qty = serializers.IntegerField()

class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.CharField()
