from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('cart-page/<pizza_uid>',views.add_cart,name='cart'),
    path('cart',views.cart,name='cart'),
    path('remove-cart-item/<cart_uuid>',views.remove_cart_item,name='remove'),
    path('order/',views.orders,name='order'),
    path('success/',views.success,name='success'),
    path('search/',views.search,name='search')
]
