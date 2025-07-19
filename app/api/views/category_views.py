from rest_framework import generics
from app.models import Category
from app.api.serializers.category_serializers import CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, FormParser] 

class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'cid'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, FormParser] 
