from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Review, Products, UserProfile
from random import randint, choice, shuffle
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the Review model with 10k unique reviews'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch products and users
        products = list(Products.objects.all())
        users = list(UserProfile.objects.all())

        if not products or not users:
            self.stdout.write(self.style.ERROR("No products or users found. Please add data first."))
            return

        # Shuffle to ensure randomization
        shuffle(products)
        shuffle(users)

        # Track unique user-product pairs
        existing_reviews = set(
            Review.objects.values_list("user_id", "product_id")
        )

        words_list = ["Bengal", "Crafts", "Handicraft", "Tradition", "Artisan", "Weaving", "Embroidery", "Pottery", "Textile", "Jute", 
                      "Sari", "Bengal Tiger", "Culture", "Folk Art", "Local", "Authentic", "GI-tagged", "Handmade", "Village", "Heritage",
                      "Craftsmanship", "Artisanship", "Channapatna", "Shola", "Bamboo", "Kantha", "Pattachitra", "Murals", "Terracotta", 
                      "Bengal Silk", "Clay", "Fabric", "Dye", "Sculpture", "Madhubani", "Lacquerware", "Woodwork", "Basketry", "Glasswork", 
                      "Tanjore", "Chittaranjan", "Silk", "Batik", "Mughal", "Bengali", "Folk", "Jewelry", "Beads", "Stonework", "Carving", 
                      "Kolkata", "Gaya", "Sundarbans", "Madhubani Art", "Bengal Curry", "Rural", "Batik", "Tribal", "Bhuri", "Paintings", 
                      "Beadwork", "Wooden", "Handloom", "Cloth", "Wool", "Leather", "Chikan", "Craftsman", "Bengal Cloth", "Quilt", 
                      "Embroidery", "Glass", "Pot", "Brass", "Gold", "Copper", "Jewel", "Filigree", "Textiles", "Kalamkari"]

        reviews = []
        unique_review_count = 0
        max_attempts = 20000  # To prevent infinite loops
        attempts = 0

        while unique_review_count < 10000 and attempts < max_attempts:
            product = choice(products)
            user = choice(users)

            # Ensure uniqueness
            if (user.id, product.product_id) not in existing_reviews:
                review_text = f"{fake.sentence(ext_word_list=words_list)} The {choice(words_list)} craftsmanship is exceptional. I love the authentic feel of the {choice(words_list)}. Highly recommend this {choice(words_list)} to anyone interested in traditional {choice(words_list)}."

                random_date = fake.date_time_between(start_date="-2y", end_date="now")

                reviews.append(Review(
                    product=product,
                    user=user,
                    review=review_text,
                    timestamp=random_date  # Assigning random datetime
                ))

                existing_reviews.add((user.id, product.product_id))  # Add to the set
                unique_review_count += 1

            attempts += 1

        # Bulk create the reviews
        if reviews:
            Review.objects.bulk_create(reviews)
            self.stdout.write(self.style.SUCCESS(f'Successfully populated {unique_review_count} unique reviews'))
        else:
            self.stdout.write(self.style.WARNING("No new reviews were added."))
