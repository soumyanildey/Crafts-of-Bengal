from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.contrib import messages
from e_commerce import settings
from django.views.generic import CreateView,TemplateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from login.models import UserProfile,User,Address
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
    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name='auth/profile_Update.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        userprofile=UserProfile.objects.get(user=user)
        address=Address.objects.filter(user=userprofile)
        context['userprofile']=userprofile
        context['addresses']=address
        return context
    


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'auth/profile_update.html'
    fields = ['profile_pic', 'ph_no', 'gender']

    def get_object(self):
        """Get the UserProfile object for the current user."""
        user = self.request.user
        return UserProfile.objects.get(user=user)

    def post(self, request, *args, **kwargs):
        """Override post to manually update user data and profile."""
        # Get the user object
        user = request.user

        # Manually update the User model fields (first_name, last_name, email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.username = request.POST.get('email', user.username)
        user.email=user.username
        user.save()

        # Also handle UserProfile update (profile_pic, ph_no, gender)
        profile = self.get_object()
        profile.profile_pic = request.FILES.get('profile_pic', profile.profile_pic)
        profile.ph_no = request.POST.get('ph_no', profile.ph_no)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.save()

        # Set a success message and redirect
        messages.success(request, "Profile updated successfully!")
        return redirect('login:update_profile')  # Redirect to the same page after updating profile

    def get_success_url(self):
        """Redirect to the profile update page after successful update."""
        return reverse_lazy('update_profile')  # Redirect to the same profile update page




class AddressCreateView(LoginRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        userprofile = UserProfile.objects.get(user=user)

        # Extract data from POST request
        name = data.get('name')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')
        pincode = data.get('pincode')

        # Check if an identical address already exists for the user
        if Address.objects.filter(
            user=userprofile,
            name=name,
            address=address,
            city=city,
            state=state,
            country=country,
            pincode=pincode
        ).exists():
            # If it exists, redirect back without saving
            return HttpResponseRedirect(reverse_lazy('login:profile'))

        # If no duplicate found, create the new address
        Address.objects.create(
            user=userprofile,
            name=name,
            address=address,
            city=city,
            state=state,
            country=country,
            pincode=pincode
        )

        # Redirect to the profile page after saving the address
        return HttpResponseRedirect(reverse_lazy('login:profile'))
    



class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    template_name = 'auth/address_update.html'
    fields = ['name', 'address', 'city', 'state', 'country', 'pincode']

    def get_success_url(self):
        """Redirect to the profile update page after successful update."""
        return reverse_lazy('login:profile') # Redirect to the same profile update page


    


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('login:profile')
    
    