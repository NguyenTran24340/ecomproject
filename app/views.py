from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from app.models import Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address, Coupon
from userauths.models import ContactUs
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
import calendar
from django.db.models.functions import ExtractMonth
from django.utils import timezone
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

#Chatbot
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os



# Create your views here.
def blog(request):
    categories = Category.objects.all().annotate(product_count=Count("category"))
    context = {
        "categories": categories
    }
    return render(request, 'app/blog.html',context)

def about(request):
    categories = Category.objects.all().annotate(product_count=Count("category"))
    context = {
        "categories": categories
    }
    return render(request, 'app/about.html',context)


def index(request):
    fabric_category = Category.objects.filter(title__iexact="Fabric").first()
    wooden_category = Category.objects.filter(title__iexact="Wooden").first()
    pottery_category = Category.objects.filter(title__iexact="Pottery").first()


    fabric_products = Product.objects.filter(product_status="public", featured=True, category=fabric_category) if fabric_category else []
    wooden_products = Product.objects.filter(product_status="public", featured=True, category=wooden_category) if wooden_category else []
    pottery_products = Product.objects.filter(product_status="public", featured=True, category=pottery_category) if pottery_category else []

    categories = Category.objects.all().annotate(product_count=Count("category"))


    context = {
        "fabric_products": fabric_products,
        "wooden_products": wooden_products,
        "pottery_products": pottery_products,
        "categories": categories
    }

    return render(request, 'app/index.html', context)

# function product
def product_list_view(request):
    products = Product.objects.filter(product_status="public")
    categories = Category.objects.all().annotate(product_count=Count("category"))

     # Filter by price 
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price) #  Filter products 
        except ValueError:
            pass
    # Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")  # ?page=1
    page_obj = paginator.get_page(page_number)
    context = {
        "products":page_obj,
        "categories": categories,
        "page_obj": page_obj,
    }

    return render(request, 'app/product-list.html', context)

# Function Category
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

# function product
def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    # product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=product.pid)
    categories = Category.objects.all().annotate(product_count=Count("category"))

    p_image = product.p_images.all()

    context = {
        "p": product,
        "p_image": p_image,
        "products": products,
        "categories": categories,
    }

    return render(request, "app/product-detail.html", context)

# Function search
def search_view(request):
    query = request.GET.get("q") # Get the query string

    products = Product.objects.filter(product_status="public") 

    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by("-date")
    else:
        products = Product.objects.filter(product_status="public").order_by("-date")

    
    categories = Category.objects.all().annotate(product_count=Count("category"))

    context = {
        "products": products,
        "query": query,
        "categories": categories,
    }

    return render(request, "app/search.html", context)

# Function Cart
def add_to_cart(request):
    cart_product = {}
    product_id = str(request.GET['id']) 
    product = Product.objects.get(id=product_id)  

    cart_product[product_id] = {
    'title': request.GET['title'],
    'qty': request.GET['qty'],
    'price': str(product.price),
    'image': request.GET['image'],
    'pid': request.GET['pid'],
}


    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart_counter(request):
    total_items = len(request.session.get('cart_data_obj', {}))
    return JsonResponse({'totalcartitems': total_items})

def cart_view(request):
    categories = Category.objects.all().annotate(product_count=Count("category"))

    cart_total_amount = 0  # Tổng tiền chưa giảm
    grand_total = 0        # Tổng tiền sau khi giảm
    discount = 0
    applied_coupon = None

    if 'cart_data_obj' in request.session and request.session['cart_data_obj']:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                price = float(item['price'].replace('$', ''))
            except ValueError:
                price = 0

            cart_total_amount += int(item['qty']) * price
        grand_total = cart_total_amount

        # ===  COUPON ===
        applied_coupon = None
        discount = 0
        if request.method == "POST":
            code = request.POST.get("coupon_code")
            coupon = Coupon.objects.filter(code=code, active=True).first()
            if coupon:
                 request.session['applied_coupon_id'] = coupon.id
                 messages.success(request, f"Coupon '{coupon.code}' applied successfully.")
                 return redirect("app:cart")
            else:
                messages.warning(request, "Invalid or expired coupon.")
                return redirect("app:cart")
            
        # Get saved coupons if any
        if request.session.get("applied_coupon_id"):
            try:
                applied_coupon = Coupon.objects.get(id=request.session["applied_coupon_id"])
                discount = applied_coupon.discount
                grand_total -= discount
            except Coupon.DoesNotExist:
                pass

        return render(request, "app/cart.html", {
            "categories": categories,
            "cart_data": request.session['cart_data_obj'],
            "totalcartitems": len(request.session['cart_data_obj']),
            "cart_total_amount": cart_total_amount,  # trước khi trừ
            "grand_total": grand_total,              # đã trừ coupon
            "applied_coupon": applied_coupon,
            "discount": discount,
        })
    else:
        return render(request, "app/empty-cart.html", {"categories": categories})

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data

    cart_data = request.session.get('cart_data_obj', {})
    cart_total_amount = 0
    grand_total = 0
    discount = 0
    applied_coupon = None

    # Total product
    for p_id, item in cart_data.items():
        price_str = item['price'].replace('$', '').strip()
        cart_total_amount += int(item['qty']) * float(price_str)

    # Coupon
    if request.session.get("applied_coupon_id"):
        try:
            applied_coupon = Coupon.objects.get(id=request.session["applied_coupon_id"])
            discount = applied_coupon.discount
            grand_total = cart_total_amount - discount
            if grand_total < 0:
                grand_total = 0
        except Coupon.DoesNotExist:
            grand_total = cart_total_amount
    else:
        grand_total = cart_total_amount

    # If empty cart after remove => render return empty-cart.html
    if not cart_data:
        request.session.pop("applied_coupon_id", None)  # Remove coupon if empty cart
        html = render_to_string("app/empty-cart.html", {}, request=request)
        return JsonResponse({"data": html, "totalcartitems": 0})

    # Render  cart-list.html
    html = render_to_string("app/cart-list.html", {
        "cart_data": cart_data,
        "totalcartitems": len(cart_data),
        "cart_total_amount": cart_total_amount,
        "grand_total": grand_total,
        "discount": discount,
        "applied_coupon": applied_coupon,
    }, request=request)

    return JsonResponse({
        "data": html,
        "totalcartitems": len(cart_data)
    })


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    grand_total = 0
    discount = 0
    applied_coupon = None
 
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            price_str = item['price'].replace('$', '').strip()
            cart_total_amount += int(item['qty']) * float(price_str)

        grand_total = cart_total_amount

        if request.session.get("applied_coupon_id"):
            try:
                applied_coupon = Coupon.objects.get(id=request.session["applied_coupon_id"])
                discount = applied_coupon.discount
                grand_total -= discount
                if grand_total < 0:
                    grand_total = 0
            except Coupon.DoesNotExist:
                applied_coupon = None   

    context = render_to_string("app/cart-list.html",{
        "cart_data": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),
        "cart_total_amount": cart_total_amount,
        "grand_total": grand_total,  
        "discount": discount,     
        "applied_coupon": applied_coupon, 
    }, request=request)
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def clear_cart(request):
    #Remove cart
    if 'cart_data_obj' in request.session:
        del request.session['cart_data_obj']
    
    #Remove coupon
    if 'applied_coupon_id' in request.session:
        del request.session['applied_coupon_id']

        messages.success(request, "Your cart and coupon has been cleared.")
    return redirect('app:cart')

#Functon Checkout
@login_required
def checkout_view(request):
    cart_total_amount = 0
    grand_total = 0
    discount = 0
    applied_coupon = None
    order = None  

    if 'cart_data_obj' in request.session and request.session['cart_data_obj']:
        # Calculate the total initial product
        for p_id, item in request.session['cart_data_obj'].items():
            price = float(item['price'].replace('$', '').strip())
            quantity = int(item['qty'])
            cart_total_amount += price * quantity

        grand_total = cart_total_amount

          # If there is a coupon, discount from grand_total
        if request.session.get("applied_coupon_id"):
            try:
                applied_coupon = Coupon.objects.get(id=request.session["applied_coupon_id"])
                discount = applied_coupon.discount
                grand_total -= discount
                if grand_total < 0:
                    grand_total = 0
            except Coupon.DoesNotExist:
                applied_coupon = None

         # Create order
        order = CartOrder.objects.create(
            user=request.user,
            price=grand_total,
            order_date=timezone.now()
        )
        request.session["order_id"] = order.id
        
        #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            price = float(item['price'].replace('$', '').strip())
            quantity = int(item['qty'])
            CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO_" + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=quantity,
                price=price,
                total=price * quantity,
            )

          # Send the correct amount to PayPal
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': "%.2f" % grand_total,
            'item_name': "Order-Item-No-" + str(order.id),
            'invoice': "INVOICE_NO-" + str(order.id),
            'currency_code': "USD",
            'notify_url': f'http://{host}{reverse("app:paypal-ipn")}',
            'return_url': f'http://{host}{reverse("app:payment-completed")}',
            'cancel_url': f'http://{host}{reverse("app:payment-failed")}',
        }
        paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    else:
     # If there is no cart then redirect or report an error
        messages.warning(request, "Your cart is empty. Please add some products.")
        return redirect("app:cart")

    categories = Category.objects.all().annotate(product_count=Count("category"))
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
        active_address = None

    return render(request, "app/checkout.html", {
        "categories": categories,
        "cart_data": request.session['cart_data_obj'],
        "totalcartitems": len(request.session['cart_data_obj']),
        "cart_total_amount": cart_total_amount,
        "grand_total": grand_total,
        "discount": discount,
        "applied_coupon": applied_coupon,
        "paypal_payment_button": paypal_payment_button,
        "active_address": active_address,
    })

# Paypal
@login_required
def payment_completed_view(request):
    cart_data = request.session.get('cart_data_obj', {})
    totalcartitems = len(cart_data)
    cart_total_amount = 0
    order = None 

    for p_id, item in cart_data.items():
        price_str = item['price'].replace('$', '').strip()
        cart_total_amount += int(item['qty']) * float(price_str)

     #Coupon
    applied_coupon = None
    discount = 0
    grand_total = cart_total_amount

    if request.session.get("applied_coupon_id"):
        try:
            applied_coupon = Coupon.objects.get(id=request.session["applied_coupon_id"])
            discount = applied_coupon.discount
            grand_total -= discount
            if grand_total < 0:
                grand_total = 0
        except Coupon.DoesNotExist:
            pass
    # Update payment status
    order_id = request.session.get("order_id")
    if order_id:
        try:
            order = CartOrder.objects.get(id=order_id, user=request.user)
            order.paid_status = True
            order.save()

            # Optional: clear order_id khỏi session nếu không cần nữa
            del request.session["order_id"]
        except CartOrder.DoesNotExist:
            order = None 

    # Clear cart
    request.session.pop('cart_data_obj', None)

    #remove coupon 
    request.session.pop('applied_coupon_id', None)

    active_address = Address.objects.get(user=request.user, status=True)

    return render(request, 'app/payment-completed.html', {
        "cart_data": cart_data,
        "totalcartitems": totalcartitems,
        "cart_total_amount": cart_total_amount,
        "order": order,
        "active_address":active_address,
        "grand_total": grand_total,
        "discount": discount,
        "applied_coupon": applied_coupon,
    })

@login_required
def payment_failed_view(request):
    return render(request, 'app/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)

    #chart
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    month = []
    total_orders = []
    for i in orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    # Address
    if request.method == "POST":
        name = request.POST.get("name") 
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        new_address = Address.objects.create(
            user=request.user,
            name=name, 
            address=address,
            mobile=mobile,
        )
        messages.success(request, f"Address for {name} added successfully.")
        return redirect("app:dashboard")

    context = {
        "orders_list": orders_list,
        "orders":orders,
        "address":address,  
        "month":month,
        "total_orders":total_orders,
    }
    return render(request, 'app/dashboard.html', context)

#function checkout
def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderItems.objects.filter(order=order)

    context = {
        "order_items": order_items,
    }
    return render(request, 'app/order-detail.html', context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})

# function wishlist
@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.all()
    categories = Category.objects.all().annotate(product_count=Count("category"))
    context = {
        "w": wishlist,
        "categories":categories
    }
    return render(request, "app/wishlist.html", context)


def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)

@login_required
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist =  Wishlist.objects.filter(user=request.user)
    wishlist_d =  Wishlist.objects.get(id=pid)
    delete_product = wishlist_d.delete()

    context = {
        "bool": True,
        "w": wishlist
    }
    
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('app/wishlist-list.html', context)
    return JsonResponse({'data': t, 'w': wishlist_json})

# Function contacr
def contact(request):
    categories = Category.objects.all().annotate(product_count=Count("category"))
    context = {
        "categories": categories
    }
    return render(request, 'app/contact.html',context)

def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }
    
    return JsonResponse({"data":data})


# Load Gemini API key
print(f"DEBUG: GEMINI_API_KEY from settings: '{settings.GEMINI_API_KEY}'")

try:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in settings.")

    genai.configure(api_key=settings.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    print("DEBUG: Gemini model initialized successfully.")

except ValueError as ve:
    print(f"CONFIG ERROR: {ve}")
    gemini_model = None
except Exception as e:
    print(f"UNEXPECTED ERROR during Gemini configuration: {e}")
    gemini_model = None


@csrf_exempt
def gemini_chat_view(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_message = body.get("message", "").lower()

        if gemini_model is None:
            return JsonResponse({"reply": "Error: Gemini API is not properly configured."})

        try:
            # 🔒 STEP 0: Block external marketplace questions
            banned_keywords = ["shopee", "tiki", "amazon", "lazada"]
            if any(keyword in user_message for keyword in banned_keywords):
                return JsonResponse({
                    "reply": "Sorry, I only provide product information from our store. External platforms like Shopee or Tiki are not supported."
                })

            # 👋 STEP 1: Greeting
            if user_message in ["hi", "hello", "hey", "xin chào", "chào"]:
                return JsonResponse({
                    "reply": "Hello! How can I assist you today? We currently offer handmade products in categories such as fabric, wooden, and pottery. Which one are you interested in?"
                })

            # 📦 STEP 2: Category selection
            for category in ["fabric", "wooden", "pottery"]:
                if category in user_message:
                    products = Product.objects.filter(category__title__iexact=category, status=True)
                    if products.exists():
                        product_names = ", ".join([p.title for p in products])
                        return JsonResponse({
                            "reply": f"You selected {category}. We currently offer: {product_names}. Which product would you like to know more about?"
                        })
                    return JsonResponse({
                        "reply": f"Currently, there are no products under the {category} category."
                    })

            # 🔍 STEP 3: Match user message with product names
            products = Product.objects.filter(status=True)
            for product in products:
                product_name = product.title.lower()

                if product_name in user_message:
                    # 🎯 Discount inquiry
                    if "discount" in user_message or "sale" in user_message or "promotion" in user_message:
                        if product.old_price > product.price:
                            percent = product.get_precentage()
                            return JsonResponse({
                                "reply": f"{product.title} is currently discounted by {percent}%. Old price: ${product.old_price}, now only ${product.price}."
                            })
                        else:
                            return JsonResponse({
                                "reply": f"{product.title} is not currently on sale."
                            })

                    # 🎨 Color inquiry
                    elif "color" in user_message:
                        return JsonResponse({
                            "reply": "Color information for this product is not available yet."
                        })

                    # 📏 Size inquiry
                    elif "size" in user_message or "dimension" in user_message:
                        return JsonResponse({
                            "reply": "Size information for this product is not available yet."
                        })

                    # 💰 Price inquiry (default)
                    else:
                        return JsonResponse({
                            "reply": f"The price of {product.title} is ${product.price}."
                        })

            # 🛠️ STEP 4: Policy & support questions
            if any(word in user_message for word in ["warranty", "return", "refund", "contact", "support", "exchange"]):
                return JsonResponse({
                    "reply": "For warranty, return, or support inquiries, please visit our 'Contact' page and send us a message. Our team will assist you shortly."
                })

            # 🚚 Shipping questions
            if "shipping fee" in user_message or "delivery charge" in user_message:
                return JsonResponse({
                    "reply": "We currently offer **Free Shipping** nationwide."
                })

            if "delivery" in user_message or "how many days" in user_message or "shipping time" in user_message:
                return JsonResponse({
                    "reply": "Delivery time is **3 days** for domestic orders and **7 days** for international ones."
                })

            # 💳 Payment methods
            if "payment" in user_message or "cash on delivery" in user_message or "cod" in user_message:
                return JsonResponse({
                    "reply": "We do not support Cash on Delivery (COD). Please complete your payment online before shipment."
                })

            # 🎁 Coupons
            if "coupon" in user_message or "discount code" in user_message or "promo code" in user_message:
                return JsonResponse({
                    "reply": "Yes, we have discount codes available, and they are updated regularly. Stay tuned for new deals!"
                })

            # 🛒 Bulk order discounts
            if "bulk order" in user_message or "buy more" in user_message or "wholesale" in user_message:
                return JsonResponse({
                    "reply": "Absolutely! We offer additional discounts for bulk orders or high-value purchases."
                })

            # STEP 5: Gemini fallback for unmatched queries
            prompt = (
                "You are a virtual assistant for a handmade product store. "
                "Always follow these rules:\n"
                "- Do NOT mention external platforms like Shopee, Tiki, Lazada, or Amazon.\n"
                "- Only answer based on the available products in our database.\n"
                "- Do NOT list all products unless explicitly asked.\n"
                "- If the customer asks vague questions, request clarification.\n\n"
                f"Customer message: {user_message}"
            )
            response = gemini_model.generate_content(prompt)
            return JsonResponse({"reply": response.text})

        except Exception as e:
            print(f"Gemini API error: {e}")
            return JsonResponse({"reply": "An error occurred while calling Gemini: " + str(e)})
        

