from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Product, Order, OrderItem, Rating, Wishlist
import uuid


# ======================
# HOME PAGE
# ======================
def home(request):
    products = Product.objects.all().order_by('-id')

    cart_count = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, complete=False).first()
        if order:
            cart_count = sum(item.quantity for item in order.orderitem_set.all())

    return render(request, 'home.html', {
        'products': products,
        'cart_count': cart_count
    })


# ======================
# PRODUCT DETAIL
# ======================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    ratings = Rating.objects.filter(product=product)

    return render(request, 'product_detail.html', {
        'product': product,
        'ratings': ratings
    })


# ======================
# ADD TO CART
# ======================
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    order, created = Order.objects.get_or_create(
        user=request.user,
        complete=False
    )

    order.item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if not created:
        order.item.quantity += 1
        order.item.save()

    messages.success(request, "Item added to cart successfully!")
    return redirect('cart')


# ======================
# CART PAGE
# ======================
@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, complete=False).first()

    if not order:
        return render(request, 'cart.html', {
            'items': [],
            'total': 0,
            'total_items': 0
        })

    items = order.orderitem_set.select_related('product')
    total = sum(item.product.price * item.quantity for item in items)
    total_items = sum(item.quantity for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total,
        'total_items': total_items,
        'order': order
    })


# ======================
# INCREASE QUANTITY
# ======================
@login_required
def increase_quantity(request, id):
    item = get_object_or_404(OrderItem, id=id)
    item.quantity += 1
    item.save()
    return redirect('cart')


# ======================
# DECREASE QUANTITY
# ======================
@login_required
def decrease_quantity(request, id):
    item = get_object_or_404(OrderItem, id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# ======================
# REMOVE ITEM
# ======================
@login_required
def remove_item(request, id):
    item = get_object_or_404(OrderItem, id=id)
    item.delete()
    return redirect('cart')
# ======================
# CHECKOUT (Payment Simulation)
# ======================
@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, complete=False).first()

    if not order:
        messages.error(request, "Your cart is empty!")
        return redirect('home')

    order_items = order.orderitem_set.all()
    order_total = order.get_total()

    if request.method == "POST":
        order.complete = True
        order.payment_status = "Paid"
        order.transaction_id = str(uuid.uuid4())
        order.save()

        messages.success(request, "Payment Successful!")
        return render('home')

    return render(request, "checkout.html", {
        "order": order,
        "order_total": order_total
    })
@login_required
def payment_success(request):
    return render(request, "payment_success.html")


# ======================
# ADD RATING
# ======================
@login_required
def add_rating(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        Rating.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            review=review
        )

        messages.success(request, "Thank you for your review!")
        return redirect('product_detail', id=id)


# ======================
# ADD TO WISHLIST
# ======================
@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(request, "Added to wishlist!")
    return redirect('home')


# ======================
# PROFESSIONAL REGISTER
# ======================
def register(request):
    if request.method == "POST":

        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password Match Check
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Username Exists Check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        # Email Exists Check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.save()

        login(request, user)

        messages.success(request, "Account created successfully!")
        return redirect('home')

    return render(request, 'register.html')