from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
import datetime, random
from cart.models import Cart
from .models import Order,OrderItem,OrderProfile
from django.shortcuts import get_object_or_404
from login.models import UserProfile,Address
from e_commerce.settings import LOGIN_URL
from django.contrib.auth.decorators import login_required
from products.models import Products
# Create your views here.

# @login_required(login_url=LOGIN_URL)
def index(request):
    rawcart = Cart.objects.filter(user=get_object_or_404(UserProfile,user=request.user))
    for item in rawcart:
        if item.quantity > item.product.product_quantity:
            Cart.objects.delete(id=item.product.product_id)
    cartitems = Cart.objects.filter(user=get_object_or_404(UserProfile,user=request.user))
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.product_price*item.quantity
    print(total_price)
    userprofile = OrderProfile.objects.filter(user=get_object_or_404(UserProfile,user=request.user)).first()
    addresses=Address.objects.filter(user=get_object_or_404(UserProfile, user=request.user))    
    context = {'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile, 'addresses':addresses}
    return render(request,"Cart/checkout.html",context)

@login_required(login_url=LOGIN_URL)
def placeorder(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cart = Cart.objects.filter(user=user_profile)
    print(f"fname: {request.POST.get('fname')}, lname: {request.POST.get('lname')}")

    if not cart.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart')
 
    
    if request.method == 'POST':
        cuser = user_profile.user
        
        if not cuser.first_name:
            cuser.first_name = request.POST.get('fname')
            cuser.last_name = request.POST.get('lname')
            cuser.save()
        
        orderprofile, created = OrderProfile.objects.get_or_create(user=user_profile)
        
        orderprofile.email = request.POST.get('email')
        orderprofile.fname = request.POST.get('fname')
        orderprofile.lname = request.POST.get('lname')
        orderprofile.phone = request.POST.get('phone')
        orderprofile.address = request.POST.get('address')
        orderprofile.city = request.POST.get('city')
        orderprofile.pincode = request.POST.get('pincode')
        orderprofile.state = request.POST.get('state')
        orderprofile.country = request.POST.get('country')
        orderprofile.save()
        
        
        cart_total_price = sum(item.product.product_price * item.quantity for item in cart)
        
        track_no = f"COBID{datetime.datetime.now().strftime('%d%m%y')}{random.randint(100000, 999999)}"
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = f"COBID{datetime.datetime.now().strftime('%d%m%y')}{random.randint(100000, 999999)}"


        fullname = request.POST.get('full_name', '').strip()
        parts = fullname.split()
        fname = parts[0] if len(parts) > 0 else ''
        lname = parts[1] if len(parts) > 1 else ''
        
        neworder = Order.objects.create(
            user=user_profile,
            fname=fname,
            lname=lname,
            email=request.POST.get('email_order'),
            phone=request.POST.get('phone_order'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            pincode=request.POST.get('pincode'),
            state=request.POST.get('state'),
            country=request.POST.get('country'),
            payment_mode=request.POST.get('payment_mode'),
            total_price=cart_total_price,
            tracking_no=track_no
        )
        print(neworder.fname,neworder.lname)
        order_items = [
            OrderItem(
                order=neworder,
                product=item.product,
                price=item.product.product_price,
                quantity=item.quantity
            ) for item in cart
        ]
        OrderItem.objects.bulk_create(order_items)
        
        for item in cart:
            item.product.product_quantity -= item.quantity
            item.product.save()
        
        cart.delete()
        messages.success(request, 'Your Order has been placed Successfully')
    
    orders = Order.objects.filter(user=user_profile).order_by('-created_at')
    return render(request, "Cart/myorders.html", {'orders': orders})


@login_required(login_url=LOGIN_URL)
def myorders(request):
    # Check if the request comes from browser back button
    
    orders = Order.objects.filter(user=get_object_or_404(UserProfile, user=request.user)).order_by('-created_at')

    context = {'orders':orders}
    return render(request,"Cart/myorders.html",context)

@login_required(login_url=LOGIN_URL)
def vieworder(request,t_no):
    
    order = Order.objects.filter(tracking_no=t_no).filter(user=get_object_or_404(UserProfile,user=request.user)).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order,'orderitems':orderitems}
    return render(request,"Cart/detailorder.html",context)
