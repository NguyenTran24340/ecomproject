

from rest_framework import generics, permissions
from app.models import Wishlist
from app.api.serializers.wishlist_serializers import WishlistSerializer

class WishlistListCreateAdminView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class WishlistRetrieveDestroyAdminView(generics.RetrieveDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
 
