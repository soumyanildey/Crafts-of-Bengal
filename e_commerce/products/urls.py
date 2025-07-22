from django.urls import path
from products import views
from django.conf.urls.static import static
from django.conf import settings
app_name='products'
urlpatterns=[
    path('santipur',views.SantipurView.as_view(),name='santipur'),
    path('santiniketan',views.SantiniketanView.as_view(),name='santiniketan'),
    path('kathi',views.KathiView.as_view(),name='kathi'),
    path('baluchari',views.BaluchariView.as_view(),name='baluchari'),
    path('teracotta',views.ChhouView.as_view(),name='chhou'),
    path('chhou',views.TeracottaView.as_view(),name='teracotta'),
    # Other URLs
    path('compare/<int:product1_id>/<int:product2_id>/', views.compare, name='compare'),
    path('search/', views.ProductSearchView.as_view(), name='search'),
    path('imageSearch/',views.ImageSearchView.as_view(),name='imageSearch'),
    path('<pk>/', views.ProductDetailView.as_view(),name='detail'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


