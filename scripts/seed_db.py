import os
import django

# Ensure DJANGO_SETTINGS_MODULE is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')

# Initialize Django
django.setup()

from store.models import Category, Product

def run():
    # Seed the database with a default category
    category, _ = Category.objects.get_or_create(id=1, name="Default Category")

    # Seed the database with a test product
    Product.objects.get_or_create(
        id=1, name="Test Product", category=category, price=10.0
    )

if __name__ == "__main__":
    run()
