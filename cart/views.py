from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import Cart
from products.models import Products
from django.contrib.auth.decorators import login_required
from e_commerce.settings import LOGIN_URL
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from login.models import UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime, random
# Create your views here.


class CartView(LoginRequiredMixin,ListView):
    template_name='Cart/cart.html'
    model=Cart
    context_object_name='cart'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=UserProfile.objects.get(user=self.request.user)
        filtered_cart = Cart.objects.filter(user=user)
        context['cart'] = filtered_cart
        return context



@login_required(login_url=LOGIN_URL)
def remove_from_cart(request,product_id):
    cart_item=Cart.objects.get(id=product_id)
    cart_item.delete()
    return redirect ('cart:cart')

@login_required(login_url=LOGIN_URL)
def add_to_cart(request,product_id):
    product=Products.objects.get(product_id=product_id)
    user=get_object_or_404(UserProfile,user=request.user)
    if product.product_quantity == 0:
        messages.error(request, 'Product is out of stock')
        return redirect('products:detail', pk=product.product_id)
    cart_item,created=Cart.objects.get_or_create(product=product,user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    # return redirect ('cart:cart')
    
    return redirect('products:detail', pk=product.product_id)

@login_required(login_url=LOGIN_URL)
def increase_quantity(request, product_id):
    cart_item=Cart.objects.get(id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:cart')

@login_required(login_url=LOGIN_URL)
def decrease_quantity(request, product_id):
    cart_item=Cart.objects.get(id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart')

@login_required(login_url=LOGIN_URL)
def buy_now(request,product_id):
    product=Products.objects.get(product_id=product_id)
    user=get_object_or_404(UserProfile,user=request.user)
    if product.product_quantity == 0:
        messages.error(request, 'Product is out of stock')
        return redirect('products:detail', pk=product.product_id)
    cart_item,created=Cart.objects.get_or_create(product=product,user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect ('cart:cart')
    





