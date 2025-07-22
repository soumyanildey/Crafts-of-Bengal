from django.db import models
from login.models import UserProfile
from products.models import Products

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added=models.DateTimeField(auto_now_add=True)
    
    


    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'
    

    def get_unit_price(self):
        return self.product.product_price
    
    def get_total_price(self):
        return self.quantity * self.product.product_price
    
    def total_amount_payable(self):
        return sum(cart.get_total_price() for cart in Cart.objects.all())
    