from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.RESTRICT)
    profile_pic=models.ImageField(upload_to='Profile_Pic',blank=True)
    ph_no=models.PositiveIntegerField()
    choices=(
             ('M','Male'),
             ('F','Female'),
             ('O','Others'))
    gender=models.CharField(choices=choices,max_length=20)



    def __str__(self):
        return self.user.username


class Address(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    pincode=models.PositiveIntegerField(max_length=6)


    def save(self, *args, **kwargs):
        if not self.name:  # Set default name dynamically before saving
            self.name = f"{self.user.user.first_name} {self.user.user.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user.first_name} {self.user.user.last_name} - {self.address}"

    
