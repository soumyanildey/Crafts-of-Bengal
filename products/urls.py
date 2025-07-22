from django.urls import path
from products import views
from django.conf.urls.static import static
from django.conf import settings
app_name='products'
urlpatterns=[
    #------redundant urls-------#
    # path('santipur/',views.SantipurView.as_view(),name='santipur'),
    # path('santiniketan/',views.SantiniketanView.as_view(),name='santiniketan'),
    # path('kathi/',views.KathiView.as_view(),name='kathi'),
    # path('baluchari/',views.BaluchariView.as_view(),name='baluchari'),
    # path('garad/', views.GaradView.as_view(), name='garad'),
    # path('chhou/',views.ChhouView.as_view(),name='chhou'),
    # path('teracotta/',views.TeracottaView.as_view(),name='teracotta'),
    # path('dokra/', views.DokraView.as_view(), name='dokra'),
    # path('kantha/', views.KanthaView.as_view(), name='kantha'),
    # path('patachitra/', views.PatachitraView.as_view(), name='patachitra'),
    # path('honey/', views.HoneyView.as_view(), name='honey'),


    path('<str:category_type>/', views.ProductView.as_view(), name='products'),
    path('compare/<int:product1_id>/<int:product2_id>/', views.compare, name='compare'),
    path('search', views.ProductSearchView.as_view(), name='search'),
    path('imageSearch',views.ImageSearchView.as_view(),name='imageSearch'),
    path('product/<pk>/', views.ProductDetailView.as_view(),name='detail'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


