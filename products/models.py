from django.db import models
from login.models import UserProfile
# Create your models here.
class Seller(models.Model):
    seller_id=models.CharField(max_length=1200)
    seller_name=models.CharField(max_length=120)
    seller_address=models.TextField()
    seller_contact=models.PositiveIntegerField()
    seller_email=models.EmailField()

    def __str__(self):
        return self.seller_id

class Category(models.Model):
    Type=models.CharField(max_length=256)

    def __str__(self):
        return self.Type
    
class SuperCategory(models.Model):
    Name=models.CharField(max_length=256)
    Category=models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.Name

class Products(models.Model):
    product_id=models.CharField(max_length=1200,primary_key=True)
    product_name=models.CharField(max_length=500)
    product_type=models.ForeignKey(Category,on_delete=models.PROTECT)
    product_price=models.FloatField()
    product_description=models.TextField(blank=True)
    product_image=models.ImageField(upload_to='product')
    product_seller=models.ForeignKey(Seller,on_delete=models.PROTECT)
    product_quantity=models.PositiveIntegerField(null=True)
    product_purchase_freq=models.PositiveIntegerField(null=True)
    date_added=models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.product_id
    

class Rating(models.Model):
    product=models.ForeignKey(Products, on_delete=models.PROTECT)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,related_name='blog_ratings')
    rating=models.PositiveIntegerField()
    

    def __str__(self):
        return str(self.product) + " " + str(self.rating)
    @classmethod
    def get_avg_rating(cls, product):
        return cls.objects.filter(product=product).aggregate(
            avg_rating=models.Avg('rating')
        )['avg_rating']
    
    @classmethod
    def get_rating_count(cls, product):
        return cls.objects.filter(product=product).count()

class Review(models.Model):
    product=models.ForeignKey(Products, on_delete=models.PROTECT)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, related_name='blog_reviews')
    review=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.product) 
    
    @classmethod
    def get_review_count(cls, product):
        return cls.objects.filter(product=product).count()
    

class ReviewPics(models.Model):
    review=models.ForeignKey(Review, on_delete=models.PROTECT)
    review_pics=models.ImageField(upload_to='review_pics',blank=True,null=True)

    def __str__(self):
        return str(self.review) + " " + str(self.review.user)