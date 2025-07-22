from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from products.models import Category,Products
from cart.models import Cart
from login.models import UserProfile
from e_commerce.settings import LOGIN_URL
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from itertools import zip_longest
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .faq_bot import get_bot_response



@csrf_exempt  # Optional: use only if CSRF token isn't handled via JS
@require_POST
def chatbot_handler(request):
    query = request.POST.get("chat_query", "")
    if not query:
        return JsonResponse({"response": "Please enter a message."})
    
    response = get_bot_response(query)
    return JsonResponse({"response": response})




class IndexView(TemplateView):
    template_name='Home/index.html'
    context_object_name='index_items'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['cart_item_quantity']=cart_quantity(self.request)
        category_baluchari = Category.objects.get(Type='Baluchari')
        category_santipur=Category.objects.get(Type='Santipur')
        category_rosogolla=Category.objects.get(Type='Rasgulla')
        category_mihidana=Category.objects.get(Type='Mihidana')
        category_sitabhog=Category.objects.get(Type='Sitabhog')
        category_moya=Category.objects.get(Type='Moya')
        context['baluchari'] = Products.objects.filter(product_type=category_baluchari).annotate(rating_count=Count('rating')).order_by('-rating_count')[:9]
        context['tant']=Products.objects.filter(product_type__Type=category_santipur).annotate(rating_count=Count('rating')).order_by('-rating_count')[:9]
        context['rosogolla']=Products.objects.filter(product_type__Type=category_rosogolla).annotate(rating_count=Count('rating')).order_by('-rating_count')[:3]
        context['mihidana']=Products.objects.filter(product_type__Type=category_mihidana).annotate(rating_count=Count('rating')).order_by('-rating_count')[:2]
        context['sitabhog']=Products.objects.filter(product_type__Type=category_sitabhog).annotate(rating_count=Count('rating')).order_by('-rating_count')[:2]
        context['moya']=Products.objects.filter(product_type__Type=category_moya).annotate(rating_count=Count('rating')).order_by('-rating_count')[:2]
        context['sweets'] = list(context['rosogolla']) + list(context['mihidana']) + list(context['sitabhog']) + list(context['moya'])
        if self.request.user.is_authenticated:
            context['userprofile'] = UserProfile.objects.get(user=self.request.user)
        else:
            context['userprofile'] = None  # or handle appropriately
        return context
    

    # @csrf_exempt
    # def post(self, request, *args, **kwargs):
    #     # Handle POST request for the chat query
    #     query = request.POST.get("chat_query")
    #     if query:
    #         response = get_bot_response(query)
    #         return self.render_to_response({
    #             'chat_query': query,
    #             'chat_response': response,
    #             **self.get_context_data()  # Include context data as well
    #         })
    #     return self.get(request, *args, **kwargs)  # Handle as normal GET request if no query is provided
    

@login_required(login_url=LOGIN_URL)
def cart_quantity(request):
    user=UserProfile.objects.get(user=request.user)
    cart_item_quantity=Cart.objects.filter(user=user).count()
    return cart_item_quantity