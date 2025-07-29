from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Address
from app.api.serializers.address_serializers import AddressSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class MakeDefaultAddressView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        address_id = request.GET.get('id')
        if not address_id:
            return Response({"error": "Missing 'id' parameter"}, status=400)

        Address.objects.filter(user=request.user).update(status=False)
        updated = Address.objects.filter(user=request.user, id=address_id).update(status=True)

        if updated:
            return Response({"message": "Default address set successfully"})
        return Response({"error": "Address not found"}, status=404)
