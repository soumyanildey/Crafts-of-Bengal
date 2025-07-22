# yourapp/management/commands/increase_product_quantity.py

from django.core.management.base import BaseCommand
import random
from django.db.models import F
from products.models import Products

class Command(BaseCommand):
    help = 'Increases the quantity of 195 random products by 100 and verifies the update'

    def handle(self, *args, **kwargs):
        # Get all products with non-null quantities
        products = Products.objects.exclude(product_quantity__isnull=True)
        product_ids = list(products.values_list('product_id', flat=True))

        if len(product_ids) < 195:
            self.stdout.write(self.style.WARNING('Not enough products available to select 195 unique ones.'))
            return

        # Select 195 unique random products
        random_ids = random.sample(product_ids, 195)

        # Update quantities
        updated_count = Products.objects.filter(product_id__in=random_ids).update(
            product_quantity=F('product_quantity') + 100
        )

        # Verify if exactly 195 items were updated
        if updated_count == 195:
            self.stdout.write(self.style.SUCCESS(f'Successfully increased the quantity of 195 products by 100'))
        else:
            self.stdout.write(self.style.ERROR(f'Error: Only {updated_count} products were updated, not 195.'))
        
        # Additional verification to ensure each product has been updated correctly
        failed_updates = Products.objects.filter(product_id__in=random_ids, product_quantity__lt=100).count()
        if failed_updates > 0:
            self.stdout.write(self.style.ERROR(f'{failed_updates} products failed to have their quantity updated correctly.'))
        else:
            self.stdout.write(self.style.SUCCESS('All products have been updated correctly.'))
