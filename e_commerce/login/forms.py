from django.forms import ModelForm
from django.contrib.auth.models import User
from login.models import UserProfile

class RegisterForm(ModelForm):
    model=User
    
