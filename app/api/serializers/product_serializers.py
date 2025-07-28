from rest_framework import serializers
from app.models import Product, Category
from userauths.models import User

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='cid',
        queryset=Category.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='username', 
        queryset=User.objects.all()
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['pid', 'sku', 'date', 'updated']
