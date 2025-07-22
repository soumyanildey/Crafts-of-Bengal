from django.contrib import admin
from .models import Seller,Products,Category,Rating,Review,SuperCategory
# Register your models here.
admin.site.register(Seller)
admin.site.register(Products)
admin.site.register(SuperCategory)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Review)