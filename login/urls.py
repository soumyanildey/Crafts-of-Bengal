from django.urls import path
from login import views
from django.conf import settings
from django.conf.urls.static import static

app_name='login'

urlpatterns=[
    path('signup',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='user_login'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('update_profile', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('create_address', views.AddressCreateView.as_view(), name='create_address'),
    path('update_address/<int:pk>', views.AddressUpdateView.as_view(), name='update_address'),
    path('delete_address/<int:pk>', views.AddressDeleteView.as_view(), name='delete_address'),
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)