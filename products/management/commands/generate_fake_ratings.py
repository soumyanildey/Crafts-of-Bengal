from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Rating, Products, UserProfile
from random import randint

class Command(BaseCommand):
    help = 'Populate the Rating model with 10k fake reviews ensuring one user rates a product only once'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get all products and users
        products = list(Products.objects.all())
        users = list(UserProfile.objects.all())

        # Track already rated (user, product) pairs
        existing_ratings = set(Rating.objects.values_list("user_id", "product_id"))

        ratings = []
        while len(ratings) < 10000:
            user = users[randint(0, len(users) - 1)]
            product = products[randint(0, len(products) - 1)]
            
            # Ensure uniqueness
            if (user.id, product.product_id) not in existing_ratings:
                existing_ratings.add((user.id, product.product_id))  # Mark as rated
                rating = randint(3, 5)  # Random rating between 3 and 5

                ratings.append(Rating(
                    product=product,
                    user=user,
                    rating=rating
                ))

        # Bulk create the ratings
        Rating.objects.bulk_create(ratings)

        self.stdout.write(self.style.SUCCESS('Successfully populated 10,000 unique ratings'))
