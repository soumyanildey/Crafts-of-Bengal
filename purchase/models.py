from django.db import models
from login.models import User,UserProfile
from products.models import Products
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150,null=False)
    lname = models.CharField(max_length=150,null=False)
    email = models.EmailField(max_length=150,null=False)
    phone = models.PositiveIntegerField(null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode = models.PositiveIntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,null=True)
    orderstatuses = (
        ('Pending','Pending'),
        ('Out for Shipping','Out for Shipping'),
        ('Completed','Completed')
    )
    status = models.CharField(max_length=150,choices=orderstatuses,default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.id,self.tracking_no)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{}-{}'.format(self.order.id,self.order.tracking_no)
    
class OrderProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    phone = models.CharField(max_length=150,null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode = models.CharField(max_length=150,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username
