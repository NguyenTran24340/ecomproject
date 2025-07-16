from django.contrib import admin
from django.urls import path
from.import views
from app.views import index, product_list_view, category_list_view, category_product_list_view, product_detail_view, search_view, add_to_cart, cart_view

app_name = "app"
urlpatterns = [
    path('', index, name="index"),
    #product
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
  

    #Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    #Search 
    path("search/", search_view, name="search"),

    #add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("cart-counter/", views.cart_counter, name="cart-counter"),

    # cart url
    path("cart/", cart_view, name="cart"),

]