from django.shortcuts import render
from django.http import HttpResponse
from app.models import Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.db.models import Count
# Create your views here.
def index(request):
    fabric_category = Category.objects.filter(title__iexact="Fabric").first()
    wooden_category = Category.objects.filter(title__iexact="Wooden").first()

    fabric_products = Product.objects.filter(product_status="public", featured=True, category=fabric_category) if fabric_category else []
    wooden_products = Product.objects.filter(product_status="public", featured=True, category=wooden_category) if wooden_category else []

    context = {
        "fabric_products": fabric_products,
        "wooden_products": wooden_products,
    }

    return render(request, 'app/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status="public")
    categories = Category.objects.all().annotate(product_count=Count("category"))

    context = {
        "products":products,
        "categories": categories
    }

    return render(request, 'app/product-list.html', context)


def category_list_view(request):
   # categories = Category.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("category"))

    context = {
        "categories": categories
    }

    return render(request, 'app/category-list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid) # farbic, wooden
    products = Product.objects.filter(product_status="public", category=category)
    categories = Category.objects.all().annotate(product_count=Count("category"))

    context = {
        "category": category,
        "products": products,
        "categories": categories
    }

    return render(request, "app/category-product-list.html", context)