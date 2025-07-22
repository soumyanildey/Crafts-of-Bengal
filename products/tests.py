from django.test import TestCase
from unittest.mock import MagicMock
from datetime import datetime, timedelta

class ProductSearchViewSortTestCase(TestCase):
    
    def setUp(self):
        # Mocking the products
        self.products = [
            MagicMock(product_id="prod1", product_name="Product One", product_price=150.00, 
                      product_purchase_freq=50, date_added=datetime.now() - timedelta(days=10)),
            MagicMock(product_id="prod2", product_name="Product Two", product_price=50.00, 
                      product_purchase_freq=200, date_added=datetime.now() - timedelta(days=5)),
            MagicMock(product_id="prod3", product_name="Product Three", product_price=200.00, 
                      product_purchase_freq=10, date_added=datetime.now() - timedelta(days=15)),
        ]

    def test_sort_by_highprice(self):
        sorted_products = self.sort_results(self.products, 'highprice')
        self.assertEqual(sorted_products[0].product_id, "prod3")  # Highest price first

    def test_sort_by_lowprice(self):
        sorted_products = self.sort_results(self.products, 'lowprice')
        self.assertEqual(sorted_products[0].product_id, "prod2")  # Lowest price first

    def test_sort_by_highpopularity(self):
        sorted_products = self.sort_results(self.products, 'highpopularity')
        self.assertEqual(sorted_products[0].product_id, "prod2")  # Highest popularity first

    def test_sort_by_lowpopularity(self):
        sorted_products = self.sort_results(self.products, 'lowpopularity')
        self.assertEqual(sorted_products[0].product_id, "prod3")  # Lowest popularity first

    def test_sort_by_newest(self):
        sorted_products = self.sort_results(self.products, 'newest')
        self.assertEqual(sorted_products[0].product_id, "prod2")  # Newest product first

    def test_sort_by_oldest(self):
        sorted_products = self.sort_results(self.products, 'oldest')
        self.assertEqual(sorted_products[0].product_id, "prod3")  # Oldest product first

    def sort_results(self, products, sort):
        # This method mimics the sorting logic in your view
        def get_rating(x):
            return x.product_purchase_freq  # Simplified for popularity testing

        sorted_items = sorted(products, key={
            'lowprice': lambda x: x.product_price,
            'highprice': lambda x: -x.product_price,
            'lowpopularity': lambda x: x.product_purchase_freq,
            'highpopularity': lambda x: -x.product_purchase_freq,
            'newest': lambda x: -x.date_added.timestamp(),
            'oldest': lambda x: x.date_added.timestamp()
        }.get(sort, lambda x: -get_rating(x)))

        return sorted_items
