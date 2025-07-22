from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import TemplateView,ListView,DetailView
from products import models
from ml_model import intersec
from .models import Products,SuperCategory
from keras.preprocessing import image
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from fuzzywuzzy import process
from django.core.files.storage import FileSystemStorage
import os
import tempfile
from ml_model import ImageRecom
from django.db.models import Avg
# Create your views here.


# class SantipurView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Santipur')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Santipur')
#         })
#         return context
    
# class SantiniketanView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Santiniketan')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Santiniketan')
#         })
#         return context
    
# class KathiView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Kathi')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Kathi')
#         })
#         return context
    
# class BaluchariView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Baluchari')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Baluchari')
#         })
#         return context
    
# class ChhouView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Chhou')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Chhou')
#         })
#         return context
    
    
# class TeracottaView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Teracotta')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Teracotta')
#         })
#         return context
    
    
# class GaradView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Garad')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Garad')
#         })
#         return context
    

# class DokraView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Dokra')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Dokra')
#         })
#         return context
    
# class KanthaView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Kantha')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Kantha')
#         })
#         return context
    
# class PatachitraView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Patachitra')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Patachitra')
#         })
#         return context
    
# class HoneyView(ListView):
#     template_name = 'Product/product_list.html'
#     model = models.Category
#     context_object_name = 'category'

#     def get_queryset(self):
#         # Filter categories by Type (assuming 'Type' exists on Category model)
#         return super().get_queryset().filter(Type='Honey')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'products': models.Products.objects.filter(product_type__Type='Honey')
#         })
#         return context
    
class ProductView(ListView):
    template_name = 'Product/product_list.html'
    model = models.Category
    context_object_name = 'category'

    def get_queryset(self):
        category_type = self.kwargs.get('category_type').capitalize()
        return models.Category.objects.filter(Type=category_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_type = self.kwargs.get('category_type').capitalize()

        # Fetch sort value from the query params (default to 'highpopularity')
        sort = self.request.GET.get('sort', 'highpopularity')

        # Get the availability filter value
        availability = self.request.GET.get('availability', '')

        # Get price range filter
        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)

        # Get category filter
        category_filter = self.request.GET.get('category_filter', '')

        # Fetch products and apply sorting
        products = self.sort_products(category_type, sort)

        # Apply availability filter
        if availability == 'in':
            products = products.filter(product_quantity__gt=0)
        elif availability == 'out':
            products = products.filter(product_quantity=0)

        # Apply price range filter
        if min_price and max_price:
            products = products.filter(product_price__gte=min_price, product_price__lte=max_price)
        elif min_price:
            products = products.filter(product_price__gte=min_price)
        elif max_price:
            products = products.filter(product_price__lte=max_price)

        # Apply category filter
        if category_filter:
            products = products.filter(product_type__Type=category_filter)

        # Context for template
        context.update({
            'products': products,
            'sort': sort,
            'category_type': category_type,
            'availability': availability,
            'min_price': min_price,
            'max_price': max_price,
            'category_filter': category_filter,
            'categories': SuperCategory.objects.values('Name').distinct()
        })

        return context

    def sort_products(self, category_type, sort):
        queryset = models.Products.objects.filter(product_type__Type=category_type)

        if sort == 'lowprice':
            return queryset.order_by('product_price')
        elif sort == 'highprice':
            return queryset.order_by('-product_price')
        elif sort == 'lowpopularity':
            return queryset.annotate(avg_rating=Avg('rating__rating')).order_by('avg_rating')
        elif sort == 'highpopularity':
            return queryset.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')
        elif sort == 'newest':
            return queryset.order_by('-date_added')
        elif sort == 'oldest':
            return queryset.order_by('date_added')
        else:
            return queryset.order_by('-avg_rating')  # Default
    

class ProductDetailView(DetailView):
    model=models.Products
    template_name='Product/product_details.html'
    
    lookup_field = 'pk'

    def get_context_data(self, **kwargs):
      context = super(ProductDetailView, self).get_context_data(**kwargs)
      current_product = self.get_object()  # This is the product object for the current page
        
        # Get the product name of the current item
      current_product_name = getattr(current_product, 'product_name', None)
      
      print(current_product_name)
      if current_product_name is None:
            # Handle missing product_name gracefully
            context['recommended_items'] = []
            return context
      
      try:
            recommended_products = intersec.load_model_results(current_product_name)
            # print(f"Recommended products for '{current_product_name}': {recommended_products}")
            context['recommended_items'] = models.Products.objects.filter(
                product_name__in=recommended_products
            )
      except Exception as e:
            # Handle errors in recommendation logic gracefully
            print(f"Error loading recommended products: {e}")
            context['recommended_items'] = []


      context['rating']=round(models.Rating.get_avg_rating(current_product),2)
      context['rating_count']=models.Rating.get_rating_count(current_product)
      context['review_count']=models.Review.get_review_count(current_product)
      context['reviews']=models.Review.objects.filter(product=current_product).order_by('-timestamp')[:5]

      return context
    
from django.shortcuts import render, get_object_or_404
# from .models import Product

def compare(request, product1_id, product2_id):
    product1 = get_object_or_404(Products, id=product1_id)
    product2 = get_object_or_404(Products, id=product2_id)
    return render(request, 'products/compare.html', {
        'product1': product1,
        'product2': product2
    })


# class SearchView(ListView):
#     template_name = 'Product/search.html'
#     model = models.Products
#     context_object_name = 'all_search_items'

#     def get_queryset(self):
#         query = self.request.GET.get('search')
#         if query:
#             return models.Products.objects.filter(product_name__icontains=query)
#         else:
#             return models.Products.objects.none()


# myapp/views.py



class ProductSearchView(SearchView):
    template_name = 'search/search.html'
    context_object_name = 'all_search_items'

    def get_queryset(self):
        query = self.request.GET.get('search', '').strip()
        sort = self.request.GET.get('sort', 'highpopularity')
        availability = self.request.GET.get('availability', '')
        min_price = self.request.GET.get('min_price', None)
        max_price = self.request.GET.get('max_price', None)
        category_filter = self.request.GET.get('category_filter', '')

        # Debugging: Check the search query and sort parameters
        print(f"Search Query: '{query}', Sort: '{sort}'")

        if not query:
            print("No query provided. Returning empty list.")
            return []

        try:
            all_items = SearchQuerySet().all()
            print(f"Found {len(all_items)} items in the search index.")

            matched_items = []
            
            for item in all_items:
                product_name = getattr(item.object, 'product_name', '')
                product_desc = getattr(item.object, 'product_description', '')

                # Debugging: Print product name and description
                print(f"Checking item: {product_name}, {product_desc}")

                name_score = process.extractOne(query, [product_name])[1] if product_name else 0
                desc_score = process.extractOne(query, [product_desc])[1] if product_desc else 0
                max_score = max(name_score, desc_score)

                # Debugging: Show name_score, desc_score, and max_score
                print(f"Name Score: {name_score}, Description Score: {desc_score}, Max Score: {max_score}")

                if max_score > 55:
                    matched_items.append((item.object, max_score))

            # Debugging: Check matched items before removing duplicates
            print(f"Matched {len(matched_items)} items before removing duplicates.")

            # Remove duplicates by primary key
            seen = set()
            unique_items = []
            for obj, score in sorted(matched_items, key=lambda x: x[1], reverse=True):
                if obj.pk not in seen:
                    seen.add(obj.pk)
                    unique_items.append(obj)

            # Debugging: Check unique items after duplicates removal
            print(f"Unique items: {len(unique_items)} after removing duplicates.")

            # Fallback: if no fuzzy match, use default search
            if not unique_items:
                fallback_items = [item.object for item in SearchQuerySet().filter(content=query)]
                print(f"Fallback found {len(fallback_items)} items.")
                unique_items = fallback_items

            # Apply additional filters on the matched items
            filtered_items = self.apply_filters(unique_items, availability, min_price, max_price, category_filter)

            return self.sort_results(filtered_items, sort)

        except Exception as e:
            print(f"Error during search query processing: {e}")
            return []

    def apply_filters(self, items, availability, min_price, max_price, category_filter):
        # Convert min_price and max_price to float if they are not None
        if min_price:
            min_price = float(min_price)
        if max_price:
            max_price = float(max_price)

        # Debugging: print before applying filters
        print(f"Applying filters: Availability: {availability}, Min Price: {min_price}, Max Price: {max_price}, Category: {category_filter}")

        if availability == 'in':
            items = [item for item in items if item.product_quantity > 0]
        elif availability == 'out':
            items = [item for item in items if item.product_quantity == 0]

        # Apply price range filter
        if min_price is not None and max_price is not None:
            items = [item for item in items if min_price <= item.product_price <= max_price]
        elif min_price is not None:
            items = [item for item in items if item.product_price >= min_price]
        elif max_price is not None:
            items = [item for item in items if item.product_price <= max_price]

        # Apply category filter
        if category_filter:
            items = [item for item in items if item.product_type.Type == category_filter]

        # Debugging: print items after filtering
        print(f"Filtered items: {len(items)}")
        return items


    def sort_results(self, items, sort):
        def get_rating(x): return x.get_avg_rating() if hasattr(x, 'get_avg_rating') else 0

        # Debugging: Log the number of items before sorting and the sorting method
        print(f"Sorting {len(items)} items by: {sort}")
        
        sorted_items = sorted(items, key={
            'lowprice': lambda x: x.product_price,
            'highprice': lambda x: -x.product_price,
            'lowpopularity': get_rating,
            'highpopularity': lambda x: -get_rating(x),
            'newest': lambda x: -x.date_added.timestamp(),
            'oldest': lambda x: x.date_added.timestamp()
        }.get(sort, lambda x: -get_rating(x)))

        # Debugging: Check if sorting worked as expected
        print(f"Sorted {len(sorted_items)} items.")
        return sorted_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Debugging: Check what is in the context before rendering
        print(f"Context before rendering: {context}")
        
        context.update({
            self.context_object_name: self.get_queryset(),
            'query': self.request.GET.get('search', ''),
            'sort': self.request.GET.get('sort', 'highpopularity'),
            'availability': self.request.GET.get('availability', ''),
            'min_price': self.request.GET.get('min_price', None),
            'max_price': self.request.GET.get('max_price', None),
            'category_filter': self.request.GET.get('category_filter', ''),
            'search_performed': bool(self.request.GET.get('search')),
        })

        # Debugging: Check the updated context
        print(f"Context after updating with search results: {context}")

        return context




    

class ImageSearchView(TemplateView):
    template_name = 'search/search.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        sort = request.GET.get('sort', 'highpopularity')

        image_file = request.FILES.get('image')
        if not image_file:
            context['all_search_items'] = []
            context['sort'] = sort
            return self.render_to_response(context)

        temp_path = self.save_temp_image(image_file)
        if not temp_path:
            context['all_search_items'] = []
            return self.render_to_response(context)

        try:
            # Getting recommendations based on the uploaded image
            results = ImageRecom.get_recommendations(temp_path)
            products = list(models.Products.objects.filter(product_image__in=results))
            # Sorting the results according to the selected sort option
            sorted_products = self.sort_results(products, sort)
            context['all_search_items'] = sorted_products
        except Exception as e:
            context['all_search_items'] = []
            print(f"Error during recommendation or sorting: {e}")
        finally:
            os.remove(temp_path)  # Clean up the temporary image file

        context['sort'] = sort  # Include the selected sort in the context for template
        return self.render_to_response(context)

    def save_temp_image(self, image):
        try:
            # Saving the uploaded image as a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                return temp_file.name
        except Exception as e:
            print(f"Error saving temp image: {e}")
            return None

    def sort_results(self, items, sort):
        # Sort the products based on the selected sort option
        def get_rating(x): 
            return x.get_avg_rating() if hasattr(x, 'get_avg_rating') else 0

        sort_criteria = {
            'lowprice': lambda x: x.product_price,
            'highprice': lambda x: -x.product_price,
            'lowpopularity': get_rating,
            'highpopularity': lambda x: -get_rating(x),
            'newest': lambda x: -x.date_added.timestamp(),
            'oldest': lambda x: x.date_added.timestamp()
        }

        # Using .get to safely fetch the sorting function, with a fallback for 'highpopularity'
        return sorted(items, key=sort_criteria.get(sort, lambda x: -get_rating(x)))