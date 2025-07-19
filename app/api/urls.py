from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.views.category_views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDeleteView
)
from app.api.views.product_views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    # Category
    path('categories/', CategoryListCreateView.as_view(), name='api-category-list-create'),
    path('categories/<str:cid>/', CategoryRetrieveUpdateDeleteView.as_view(), name='api-category-rud'),

    # Product
    path('', include(router.urls)),
]
