from django.urls import path
from . import views
app_name='purchase'

urlpatterns=[
    path('checkout',views.index,name="checkout"),
    path('placeorder',views.placeorder,name="placeorder"),
    path('myorders',views.myorders,name="myorders"),
    path('vieworder/<str:t_no>',views.vieworder,name="orderview"),
]