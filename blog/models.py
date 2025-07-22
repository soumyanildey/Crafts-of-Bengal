from django.db import models
from login.models import UserProfile
from django.conf import settings
# Create your models here.



class Author(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    author_pic = models.ImageField(upload_to='author_pics', blank=True, null=True)


    def __str__(self):
        return str(self.user)
    
class Category(models.Model):
    district= models.CharField(max_length=100)
    item_name= models.CharField(max_length=100)
    
    def __str__(self):
        return self.district + ' - ' + self.item_name
    

class Tag(models.Model):
    name=models.CharField(max_length=20)




class Blog(models.Model):
    title=models.TextField()
    slug=models.SlugField(unique=True)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    excerpt=models.CharField(max_length=150)
    content=models.TextField()
    image=models.ImageField()
    tags=models.ManyToManyField(Tag, blank=True)
    date_posted=models.DateField(auto_now=True)
    time_posted=models.TimeField(auto_now=True)
    is_published=models.BooleanField(default=False)

    
    def __str__(self):
        return self.title
    
    def get_author(self):
        return self.author.user.name
    
    def get_time(self):
        return self.time_posted
    
    def get_date(self):
        return self.date_posted
    
    def get_avg_rating(self):
        ratings=Rating.objects.filter(blog=self).aggregate(models.Avg('rating'))
        return ratings['rating__avg'] or 0
    
    def get_total_reviews(self):
        return Review.objects.filter(blog=self).count()


class Rating(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='product_ratings')
    rating=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('blog', 'user')


class Review(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='product_reviews')
    content=models.TextField()
    date_posted=models.DateField(auto_now=True)
    time_posted=models.TimeField(auto_now=True)
    
    class Meta:
        unique_together=('blog', 'user')