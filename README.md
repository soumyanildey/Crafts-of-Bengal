# Crafts of Bengal - E-commerce Platform

An e-commerce platform dedicated to showcasing and selling traditional crafts and products from Bengal. This project combines modern web technologies with machine learning to provide a seamless shopping experience.

## Features

### User Management
- User registration and authentication
- Profile management with profile pictures
- Address management for shipping
- Gender selection options

### Product Catalog
- Comprehensive product listings with images, descriptions, and pricing
- Product categorization (Baluchari Sarees, Santipuri Sarees, Chhau Masks, Terracotta, Leather Bags, Madur Kathi, etc.)
- Super categories for better organization
- Product search functionality using Django Haystack with Whoosh backend
- Product filtering options

### Shopping Experience
- Shopping cart functionality
- Checkout process
- Order management and tracking
- COD payment mode options
- Order status updates (Pending, Out for Shipping, Completed)

### Reviews and Ratings
- Product rating system
- Review submission with timestamps
- Review images upload capability
- Average rating calculation

### Machine Learning Features
- Image-based product recommendations using InceptionResNetV2
- Collaborative filtering for personalized recommendations
- Matrix factorization recommender system
- Hybrid recommendation system combining multiple approaches

### Blog System
- Blog posts with authors
- Blog permissions management

### Customer Support
- FAQ chatbot using embedding transformer models
- Natural language processing for query understanding

### Search Capabilities
- Full-text search using Django Haystack
- Fuzzy search for better user experience

## Technology Stack

### Backend
- Django 4.2+
- Django REST Framework
- SQLite database (development)
- PostgreSQL database (production)

### Frontend
- HTML, CSS, JavaScript
- Django Templates

### Machine Learning & AI
- TensorFlow/Keras
- scikit-learn
- OpenCV

### Search
- Django Haystack
- Whoosh search engine

### Authentication
- Django Custom Authentication System

## Installation and Setup

### Prerequisites
- Python >=3.8,<3.12
- Poetry (dependency management)
- Docker & Docker Compose (for PostgreSQL deployment)

### Installation Steps with Poetry

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Crafts-of-Bengal.git
   cd Crafts-of-Bengal/e_commerce
   ```

2. Install Poetry if you don't have it already:
   ```
   # Windows PowerShell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

   # macOS/Linux
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies using Poetry:
   ```
   poetry install
   ```

4. Activate the Poetry virtual environment:
   ```
   poetry shell
   ```

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

### Machine Learning Model Setup

The project includes pre-trained machine learning models for recommendations. The model files are:
- `ml_model/model.keras` - Image feature extraction model
- `ml_model/Images_features.pkl` - Extracted image features
- `ml_model/filenames.pkl` - Image filenames for recommendations
- `ml_model/correlation_matrix.pkl` - For collaborative filtering
- `ml_model/ItemBase.pkl` - Item-based collaborative filtering model
- `ml_model/MatFac.pkl` - Matrix factorization model

These files should be included in the repository. If not, you'll need to train the models using the provided Jupyter notebooks in the `ml_model` directory.

#### Using feature_extractor.py

The `feature_extractor.py` script is used to create the InceptionResNetV2-based model for image feature extraction. This model is a critical component of the image-based recommendation system.

**Purpose:**
- Creates and saves a pre-trained InceptionResNetV2 model with GlobalMaxPooling2D layer
- Generates the `model.keras` file used by the recommendation system

**Usage:**
```bash
python ml_model/feature_extractor.py
```

**How it works:**
1. Loads the InceptionResNetV2 model with pre-trained ImageNet weights
2. Freezes the base model layers to preserve the pre-trained weights
3. Adds a GlobalMaxPooling2D layer to convert feature maps to feature vectors
4. Saves the model in .keras format for later use by the recommendation system

This script only needs to be run once to generate the model file, or if you want to recreate the model with different parameters.

## Project Structure

- `blog/` - Blog application
- `cart/` - Shopping cart functionality
- `contact/` - Contact form and management
- `e_commerce/` - Main project settings
- `index/` - Homepage and main views
- `login/` - User authentication and profile management
- `media/` - User-uploaded media files
- `ml_model/` - Machine learning models and utilities
- `products/` - Product catalog and management
- `purchase/` - Order processing and management
- `static/` - Static files (CSS, JS, images)
- `template/` - HTML templates
- `uploads/` - Additional upload directory
- `whoosh_index/` - Search index files

## Usage

### Admin Interface

Access the admin interface at http://127.0.0.1:8000/admin/ using your superuser credentials to:
- Manage products and categories
- Handle user accounts
- Process orders
- Moderate reviews and ratings

### Shopping

1. Browse products by category
2. Use the search functionality to find specific items
3. Add products to your cart
4. Proceed to checkout
5. Enter shipping and payment information
6. Complete your purchase

### User Account

1. Register a new account
2. Update your profile information
3. Add multiple shipping addresses
4. View your order history
5. Track current orders

## Development

### Adding New Products

1. Log in to the admin interface
2. Navigate to Products > Products
3. Click "Add Product"
4. Fill in the product details and upload images
5. Save the product

### Creating Categories

1. Log in to the admin interface
2. Navigate to Products > Categories
3. Click "Add Category"
4. Enter the category name
5. Save the category

## PostgreSQL Migration for Production

### Docker Setup

1. Create a `docker-compose.yml` file in the project root:
   ```yaml
   version: '3.8'

   services:
     db:
       image: postgres:15
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       env_file:
         - ./.env
       environment:
         - POSTGRES_PASSWORD=${DB_PASSWORD}
         - POSTGRES_USER=${DB_USER}
         - POSTGRES_DB=${DB_NAME}
       ports:
         - "5432:5432"

   volumes:
     postgres_data:
   ```

2. Create a `.env` file with database credentials:
   ```
   DB_NAME=crafts_of_bengal
   DB_USER=postgres
   DB_PASSWORD=your_secure_password
   DB_HOST=db
   DB_PORT=5432
   ```

3. Update `settings.py` to use PostgreSQL in production:
   ```python
   import os
   from pathlib import Path
   from dotenv import load_dotenv

   load_dotenv()

   # Database configuration
   if os.environ.get('ENVIRONMENT') == 'production':
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': os.environ.get('DB_NAME'),
               'USER': os.environ.get('DB_USER'),
               'PASSWORD': os.environ.get('DB_PASSWORD'),
               'HOST': os.environ.get('DB_HOST', 'db'),
               'PORT': os.environ.get('DB_PORT', '5432'),
           }
       }
   else:
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.sqlite3',
               'NAME': BASE_DIR / 'db.sqlite3',
           }
       }
   ```

4. Start the PostgreSQL container:
   ```
   docker-compose up -d
   ```

5. Run migrations with PostgreSQL:
   ```
   ENVIRONMENT=production python manage.py migrate
   ```

### Performance Optimizations

1. Add database indexes for frequently queried fields in models:
   ```python
   class Products(models.Model):
       # Existing fields...
       class Meta:
           indexes = [
               models.Index(fields=['product_type']),
               models.Index(fields=['product_price']),
           ]
   ```

2. Use Django's `select_related` and `prefetch_related` to optimize queries:
   ```python
   # Instead of
   products = Products.objects.all()

   # Use
   products = Products.objects.select_related('product_type', 'product_seller').all()
   ```

3. Consider using Django Caching for frequently accessed data:
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://redis:6379/1',
       }
   }
   ```


