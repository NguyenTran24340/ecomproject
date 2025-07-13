from django.contrib import admin
from django.urls import path
from.import views
from app.views import index, product_list_view, category_list_view, category_product_list_view, product_detail_view

app_name = "app"
urlpatterns = [
    path('', index, name="index"),

    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),

    #Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),
]