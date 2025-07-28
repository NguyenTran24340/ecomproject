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
# Wishlist  
from app.api.views.wishlist_views import (
    WishlistListCreateAdminView,
    WishlistRetrieveDestroyAdminView
)

# Order
from app.api.views.order_views import CreateOrderAPIView, OrderHistoryAPIView, OrderDetailAPIView, OrderDetailAPIView

#Payment
from app.api.views.payment_views import PaymentCreateAPIView
from app.api.views.payment_views import PaymentHistoryAPIView


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

    # Wishlist  
    path('wishlist/wishlist/', WishlistListCreateAdminView.as_view(), name='admin-wishlist-list-create'),
    path('wishlist/wishlist/<int:pk>/', WishlistRetrieveDestroyAdminView.as_view(), name='admin-wishlist-detail'),

    # Order
    path('order/create/', CreateOrderAPIView.as_view(), name='api-order-create'),
    path('order/history/', OrderHistoryAPIView.as_view(), name='api-order-history'),
    path('order/<int:id>/', OrderDetailAPIView.as_view(), name='api-order-detail'),
    path('order/<int:id>/', OrderDetailAPIView.as_view(), name='api-order-detail'),

    # Payment
    path('payment/create/', PaymentCreateAPIView.as_view(), name='api-payment-create'),
    path('payment/history/', PaymentHistoryAPIView.as_view(), name='payment-history'),
   
]
