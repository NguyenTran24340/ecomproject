from django.urls import path
from app.api.views.category_views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDeleteView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='api-category-list-create'),
    path('categories/<str:cid>/', CategoryRetrieveUpdateDeleteView.as_view(), name='api-category-rud'),
]
