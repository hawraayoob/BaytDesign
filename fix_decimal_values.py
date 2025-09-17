import os
import sys
import django
from decimal import Decimal, InvalidOperation

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Baytdesign.settings')
django.setup()

from main_app.models import Budget, Product, SelectedProduct, Cart

def fix_budget_records():
    print("Fixing Budget records...")
    budgets = Budget.objects.all()
    fixed_count = 0
    
    for budget in budgets:
        try:
            # Test if the value can be properly converted to Decimal
            test_value = Decimal(budget.total)
            # If we get here, the value is valid
        except (InvalidOperation, ValueError):
            print(f"Found invalid budget total: {budget.total} for budget ID: {budget.id}")
            # Fix the invalid value by setting it to 0
            budget.total = Decimal('0')
            budget.save()
            fixed_count += 1
    
    print(f"Fixed {fixed_count} budget records")

def fix_product_records():
    print("Fixing Product records...")
    products = Product.objects.all()
    fixed_count = 0
    
    for product in products:
        try:
            # Test if the value can be properly converted to Decimal
            test_value = Decimal(product.price)
            # If we get here, the value is valid
        except (InvalidOperation, ValueError):
            print(f"Found invalid product price: {product.price} for product ID: {product.id}")
            # Fix the invalid value by setting it to 0
            product.price = Decimal('0')
            product.save()
            fixed_count += 1
    
    print(f"Fixed {fixed_count} product records")

if __name__ == "__main__":
    print("Starting database decimal value fix script...")
    fix_budget_records()
    fix_product_records()
    print("Database fix completed.")