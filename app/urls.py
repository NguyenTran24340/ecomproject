from django.contrib import admin
from django.urls import path,include
from.import views
from app.views import about, blog, index, product_list_view, category_list_view, category_product_list_view, product_detail_view, search_view, add_to_cart, cart_view, delete_item_from_cart, update_cart, checkout_view, clear_cart, payment_completed_view, payment_failed_view, customer_dashboard, order_detail, make_address_default, wishlist_view , add_to_wishlist, remove_wishlist, contact, ajax_contact_form

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

    # Delete item form cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    # Update cart
    path("update-cart/", update_cart, name="update-cart"),

    #Clear cart
    path("clear-cart/", clear_cart, name="clear-cart"),

    # Checkout
    path("checkout/", checkout_view, name="checkout"),

    #Paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    # Payment Successful
    path("payment-completed/", payment_completed_view, name="payment-completed"),
    
    # Payment Failed
    path("payment-failed/", payment_failed_view, name="payment-failed"),
    
    # dashboard url
    path("dashboard/", customer_dashboard, name="dashboard"),

    # order detail
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),

    # Making address default
    path("make-default-address/", make_address_default, name="make-default-address"),

    # wishlist url
    path("wishlist/", wishlist_view, name="wishlist"),

    # adding to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    # Removing from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),

    # Contact
    path("contact/", contact, name="contact"),
    
    path("ajax_contact_form/", ajax_contact_form, name="ajax_contact_form"),

    # url blog, about
    path("blog/", blog, name="blog"),

    path("about/", about, name="about"),
]