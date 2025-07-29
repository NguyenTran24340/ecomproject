# app/api/views/coupon_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from app.models import Coupon
from app.api.serializers.coupon_serializers import CouponSerializer, ApplyCouponSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

# Admin CRUD ViewSet
class CouponAdminViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminUser]

# API user use code
class ApplyCouponAPIView(APIView):
    @swagger_auto_schema(request_body=ApplyCouponSerializer)
    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code'].strip()
            coupon = Coupon.objects.filter(code__iexact=code, active=True).first()
            if coupon:
                request.session['applied_coupon_id'] = coupon.id
                return Response({
                    "message": f"Coupon '{coupon.code}' applied.",
                    "discount": coupon.discount
                })
            return Response({"error": "Invalid or expired coupon."}, status=400)
        return Response(serializer.errors, status=400)
