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

    
