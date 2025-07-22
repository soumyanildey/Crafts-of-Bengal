from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch
from .models import Blog
from .serializers import BlogSerializer,BlogWriteSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Blog
from .serializers import BlogSerializer, BlogWriteSerializer, BlogUpdateSerializer, ReviewCreateSerializer,ReviewRetrieveSerializer,ReviewUpdateSerializer,ReviewSerializer
# views.py

from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializers import ReviewSerializer


# views.py

class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.select_related('author', 'category') \
                           .prefetch_related('tags', 'rating_set', 'review_set')

    def get_serializer_class(self):
        if self.action == 'create':
            return BlogWriteSerializer
        elif self.action in ['update', 'partial_update']:
            return BlogUpdateSerializer
        return BlogSerializer




class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        elif self.action == 'retrieve':
            return ReviewRetrieveSerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        return ReviewRetrieveSerializer  # fallback for list