from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:id>/', views.remove_item, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # ✅ Logout with redirect
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('register/', views.register, name='register'),
]