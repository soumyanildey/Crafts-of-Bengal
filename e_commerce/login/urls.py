from django.urls import path
from login import views
from django.conf import settings
from django.conf.urls.static import static

app_name='login'

urlpatterns=[
    path('signup',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='user_login'),
    path('logout',views.LogoutView.as_view(),name='logout'),
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)