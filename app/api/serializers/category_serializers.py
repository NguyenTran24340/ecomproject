from rest_framework import serializers
from app.models import Category

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = ['cid', 'title', 'image']
        read_only_fields = ['cid']

