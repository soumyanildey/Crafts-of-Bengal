from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import TemplateView,ListView,DetailView
from products import models
from ml_model import intersec
from .models import Products
from keras.preprocessing import image
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from fuzzywuzzy import process
from django.core.files.storage import FileSystemStorage
import os
import tempfile
from ml_model import ImageRecom
# Create your views here.


class SantipurView(ListView):
    template_name='Product/product_list.html'
    model=models.Category
    context_object_name='category'
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(Type='Santipur')
    def get_context_data(self, **kwargs):
        context = super(SantipurView, self).get_context_data(**kwargs)
        context.update({
            'items': models.Products.objects.all()
        })
        return context
    
class SantiniketanView(ListView):
    template_name='Product/product_list.html'
    model=models.Category
    context_object_name='category'
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(Type='Santiniketan')
    def get_context_data(self, **kwargs):
        context = super(SantiniketanView, self).get_context_data(**kwargs)
        context.update({
            'items': models.Products.objects.all()
        })
        return context
    
class KathiView(ListView):
    template_name='Product/product_list.html'
    model=models.Category
    context_object_name='category'
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(Type='Kathi')
    def get_context_data(self, **kwargs):
        context = super(KathiView, self).get_context_data(**kwargs)
        context.update({
            'items': models.Products.objects.all()
        })
        return context
    
class BaluchariView(ListView):
    template_name='Product/product_list.html'
    model=models.Category
    context_object_name='category'
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(Type='Baluchari')
    def get_context_data(self, **kwargs):
        context = super(BaluchariView, self).get_context_data(**kwargs)
        context.update({
            'items': models.Products.objects.all()
        })
        return context
    
class ChhouView(ListView):
    template_name='Product/product_list.html'
    model=models.Category
    context_object_name='category'
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(Type='Chhou')
    def get_context_data(self, **kwargs):
        context = super(ChhouView, self).get_context_data(**kwargs)
        context.update({
            'items': models.Products.objects.all()
        })
        return context
    
class TeracottaView(ListView):
    template_name='Product/product_list.html'
    model=models.Category
    context_object_name='category'
    def get_queryset(self):
        # original qs
        qs = super().get_queryset() 
        # filter by a variable captured from url, for example
        return qs.filter(Type='Teracotta')
    def get_context_data(self, **kwargs):
        context = super(TeracottaView, self).get_context_data(**kwargs)
        context.update({
            'items': models.Products.objects.all()
        })
        return context
    

class ProductDetailView(DetailView):
    model=models.Products
    template_name='Product/product_details.html'
    
    lookup_field = 'pk'

    def get_context_data(self, **kwargs):
      context = super(ProductDetailView, self).get_context_data(**kwargs)
      current_product = self.get_object()  # This is the product object for the current page
        
        # Get the product name of the current item
      current_product_name = getattr(current_product, 'product_name', None)
      current_product_id = getattr(current_product, 'product_id', None)
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


      context['rating']=(models.Rating.get_avg_rating(current_product))
      context['rating_count']=models.Rating.get_rating_count(current_product)
      context['review_count']=models.Review.get_review_count(current_product)
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
        query = self.request.GET.get('search', '')
        if query:
            try:
                print(f"Processing search query: {query}")
                
                # Get all items from the SearchQuerySet
                all_items = SearchQuerySet().all()
                matched_items = []

                for item in all_items:
                    try:
                        # Extract product details
                        product_name = getattr(item.object, 'product_name', '')
                        product_description = getattr(item.object, 'product_description', '')

                        # Print debug info
                        print(f"Checking item: {product_name}")
                        print(f"Description: {product_description[:100]}...")

                        # Match scores
                        name_match = process.extractOne(query, [product_name] if product_name else [''])
                        desc_match = process.extractOne(query, [product_description] if product_description else [''])

                        # Add items based on fuzzy match score
                        if (name_match and name_match[1] > 60) or (desc_match and desc_match[1] > 50):
                            matched_items.append({
                                'item': item,
                                'score': max(
                                    name_match[1] if name_match else 0,
                                    desc_match[1] if desc_match else 0
                                )
                            })

                    except Exception as e:
                        print(f"Error processing item: {e}")
                        continue

                # Sort by match score
                matched_items.sort(key=lambda x: x['score'], reverse=True)

                # Deduplicate results
                seen = set()
                final_results = []
                for matched_item in matched_items:
                    item = matched_item['item']
                    if item.pk not in seen:
                        seen.add(item.pk)
                        final_results.append(item)

                print(f"Found {len(final_results)} results for query: {query}")

                # Fallback exact search
                if not final_results:
                    exact_matches = SearchQuerySet().filter(content=query)
                    final_results = list(exact_matches)
                    print(f"Fallback exact search found {len(final_results)} results")

                return final_results

            except Exception as e:
                print(f"Search error: {e}")
                return SearchQuerySet().none()

        return SearchQuerySet().none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search', '')
        try:
            # Retrieve the search results
            queryset = self.get_queryset()

            # Update the context
            context.update({
                self.context_object_name: [item.object for item in queryset],  # Extract objects from SQS
                'query': query,
                'debug_query': query,
                'debug_results_count': len(queryset) if queryset else 0,
                'search_performed': bool(query),  # Flag for whether a search occurred
            })
        except Exception as e:
            print(f"Context error: {e}")
            context.update({
                self.context_object_name: [],  # Empty results
                'query': '',
                'debug_query': '',
                'debug_results_count': 0,
                'search_performed': False,
            })
        return context



class ImageSearchView(TemplateView):
    template_name = 'search/search.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            # Fetch the uploaded file
            image = request.FILES.get('image')
            if image:
                print(f"Received file: {image}")  # Debugging
                # Save the file temporarily
                temp_file_path = self.save_to_temp_file(image)

                if temp_file_path:
                    # Call the recommendation system with the temporary file path
                    results = ImageRecom.get_recommendations(temp_file_path)
                    print(f"Recommendations: {results}")  # Debugging

                    # Query the database for matching products
                    context['all_search_items'] = models.Products.objects.filter(product_image__in=results)
                    print(context['all_search_items'])
                    # Clean up the temporary file
                    os.remove(temp_file_path)
                else:
                    print("Failed to save the uploaded image to a temporary file.")
                    context['all_search_items'] = []
            else:
                print("No file received in the request.")
                context['all_search_items'] = []

        except Exception as e:
            print(f"Error in ImageSearchView: {e}")
            context['all_search_items'] = []

        return self.render_to_response(context)
    
    def save_to_temp_file(self, image):
        """
        Save the uploaded image to a temporary file and return its file path.
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
                print(f"Temporary file saved at: {temp_file_path}")  # Debugging
                return temp_file_path
        except Exception as e:
            print(f"Error saving temporary file: {e}")
            return None

