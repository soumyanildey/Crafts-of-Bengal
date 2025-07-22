from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, ReviewViewSet  # Import both viewsets

router = DefaultRouter()
router.register('blogs', BlogViewSet, basename='blog')
router.register('reviews', ReviewViewSet, basename='review')  # Register ReviewViewSet

urlpatterns = [
    path('', include(router.urls)),
]
