from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from products.models import Category,Products
# Create your views here.

class IndexView(TemplateView):
    template_name='Home/index.html'
    
    
