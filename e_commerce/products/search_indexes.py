# myapp/search_indexes.py
from haystack import indexes
from .models import Products

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    # Define fields to index
    text = indexes.CharField(document=True, use_template=True)  # Full-text indexing template
    product_name = indexes.CharField(model_attr='product_name')  # Product name
    description = indexes.CharField(model_attr='product_description')  # Product description
    price = indexes.FloatField(model_attr='product_price')  # Price

    def get_model(self):
        return Products

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


