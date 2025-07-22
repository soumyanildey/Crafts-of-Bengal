from rest_framework import serializers
from .models import Author, Category, Tag, Blog, Rating, Review
from login.models import UserProfile
from django.contrib.auth.models import User
from django.utils.text import slugify




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  


class UserProfileSerializer(serializers.ModelSerializer):

    user=UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'profile_pic', 'ph_no', 'gender']

class AuthorSerializer(serializers.ModelSerializer):

    user=UserProfileSerializer(read_only=True)

    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['district', 'item_name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'rating', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'content', 'date_posted', 'time_posted']

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    ratings = RatingSerializer(source="rating_set", many=True, read_only=True)  # Fetch all ratings
    reviews = ReviewSerializer(source="review_set", many=True, read_only=True)  # Fetch all reviews
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'author', 'category', 'excerpt', 'content', 'image', 'tags',
                  'date_posted', 'time_posted', 'is_published', 'avg_rating', 'total_reviews', 'ratings', 'reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_total_reviews(self, obj):
        return obj.get_total_reviews()




class BlogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'author', 'category', 'excerpt', 'content', 'image', 'tags', 'is_published']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        title = validated_data.get("title", "")
        slug_base = slugify(title)
        slug = slug_base
        counter = 1

        while Blog.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{counter}"
            counter += 1

        validated_data["slug"] = slug
        blog = Blog.objects.create(**validated_data)
        blog.tags.set(tags)
        return blog



class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'excerpt', 'content', 'image', 'tags']

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.tags.set(tags)
        instance.save()
        return instance







# Create Serializer
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'blog', 'user', 'content']
        read_only_fields = ['id']

# Retrieve Serializer
class ReviewRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'blog', 'user', 'content', 'date_posted', 'time_posted']

# Update Serializer (only allows content to be updated)
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['content']

# Delete doesn't require a separate serializer — DRF handles it
