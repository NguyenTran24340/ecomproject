from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Category
from app.api.views.category_views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDeleteView
)

# Product
from app.api.views.product_views import ProductViewSet

# Cart
from app.api.views.cart_views import (
    CartView, AddToCartView, UpdateCartView, RemoveFromCartView
)


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    # Category
    path('categories/', CategoryListCreateView.as_view(), name='api-category-list-create'),
    path('categories/<str:cid>/', CategoryRetrieveUpdateDeleteView.as_view(), name='api-category-rud'),

    # Product
    path('', include(router.urls)),

    # Cart
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/update/', UpdateCartView.as_view(), name='cart-update'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='cart-remove'),
]
