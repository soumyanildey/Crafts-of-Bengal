from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from e_commerce import settings
from django.views.generic import CreateView,TemplateView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from login.models import UserProfile,User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
# Create your views here.

# class LoginView(View):
#     template_name='Auth/login.html'
#     form_class=Login_Form


class RegisterView(TemplateView):
    template_name='auth/signup.html'
    def post(self,request):
        data=request.POST
        
        firstname=data['fname']
        lastname=data['lname']
        email=data['email']
        phno=data['cno']
        gender=data['gender']
        password=data['pw']
        
        
        user_instance=User(username=email,first_name=firstname,last_name=lastname,password=make_password(password))
        user_instance.save()
        userprofile_instance=UserProfile(user=user_instance,ph_no=phno,gender=str(gender))
        userprofile_instance.save()
        return HttpResponseRedirect(reverse_lazy('login:user_login'))

    
class LoginView(TemplateView):
    template_name='auth/login.html'
    def post(self,request):
        username=request.POST['email']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index:index'))
            else:
                return HttpResponse("User Not Active, Contact Supoort Team for Account Activation...")
        else:
            # Return an error message or redirect to login page again
            return HttpResponseRedirect(reverse('login:user_login'))
class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index:index'))