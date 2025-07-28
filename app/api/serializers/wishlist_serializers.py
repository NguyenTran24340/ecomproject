# api/serializers/wishlist_serializers.py

from rest_framework import serializers
from app.models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
