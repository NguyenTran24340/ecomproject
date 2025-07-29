from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from userauths.models import ContactUs
from app.api.serializers.contact_serializers import ContactUsSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser


class ContactFormAPIView(APIView):
    @swagger_auto_schema(request_body=ContactUsSerializer)
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactListAdminView(generics.ListAPIView):
    queryset = ContactUs.objects.all().order_by("-id")
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminUser]  
