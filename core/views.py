import uuid
from instamojo_wrapper import Instamojo
from django.shortcuts import render,redirect
from .models import Cart, CartItems, PizzCategory, Pizza,User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint="https://test.instamojo.com/api/1.1/")



def home(request):
    pizzas = Pizza.objects.all()
    return render(request,'home.html',{'pizza':pizzas})

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request,'User not found')
                return redirect(login_page)
            user_obj = authenticate(username=username,password=password)
            if user_obj:
                login(request,user_obj)
                return redirect(home)
            messages.error(request,'Wrong Password')
            return redirect(login_page) 
        except Exception as e:
            messages.error(request,'Something went wrong')
            return redirect(register_page)
    return render(request,'login.html')

def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request,'This username is already taken please try with new username')
                return redirect(register_page)
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,'Account has been created')
            return redirect(login_page) 
        except Exception as e:
            messages.error(request,'Something went wrong')
            return redirect(register_page)
    return render(request,'register.html')
    
@login_required(login_url=login_page)
def add_cart(request,pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid = pizza_uid)
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_item = CartItems.objects.create(
        cart = cart,
        pizza = pizza_obj
    )
    return redirect('/')

@login_required(login_url=login_page)
def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    response = api.payment_request_create(
        amount = cart.get_total(),
        purpose = 'order',
        buyer_name = request.user.username,
        email='raorudhra16@gmail.com',
        redirect_url="http://127.0.0.1:8000/success/"
    )
    cart.instamojo_id = response['payment_request']['id']
    cart.save()
    return render(request,'cart.html',{'cart':cart,'payment_url':response['payment_request']['longurl']})

@login_required(login_url=login_page)
def remove_cart_item(request,cart_uuid):
    try:
        CartItems.objects.get(uid=cart_uuid).delete()
        return redirect(cart)
    except Exception as e:
        print(e)

@login_required(login_url=login_page)
def orders(request):
    order = Cart.objects.filter(is_paid=True,user=request.user)
    return render(request,'order.html',{'order':order})

@login_required(login_url=login_page)
def success(request):
    payment_request = request.GET.get('payment_request_id')
    cart = Cart.objects.get(instamojo_id=payment_request)
    cart.is_paid = True
    cart.save()
    return redirect(orders)


def search(request):
    query  =  request.GET['query']
    # pizza_category  =  PizzCategory.objects.filter(category_name__icontains=query)
    pizza_names = Pizza.objects.filter(pizza_name__icontains=query)
    result = pizza_names
    return render(request,'search.html',{'result':result})