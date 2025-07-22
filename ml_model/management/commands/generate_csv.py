# your_app/management/commands/generate_csv.py
import csv
from django.core.management.base import BaseCommand
from login.models import UserProfile  # Adjusted import
from products.models import Rating,Products

class Command(BaseCommand):
    help = 'Generates a CSV of User_id, Product Name, and Rating for ML model training'

    def handle(self, *args, **kwargs):
        # Query the ratings data, adjusted to include related fields
        ratings = Rating.objects.all().select_related('user', 'product')

        # Create or overwrite the CSV file
        with open('ratings_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['User_id', 'Product Name', 'Rating'])  # Header row
            
            for rating in ratings:
                # Write each row: User_id, Product Name, and Rating
                writer.writerow([rating.user.user_id, rating.product.product_name, rating.rating])

        self.stdout.write(self.style.SUCCESS('Successfully generated ratings_data.csv'))
