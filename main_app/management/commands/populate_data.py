from django.core.management.base import BaseCommand
from main_app.models import Classification, Shop, Product, BudgetEstimate

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create Classifications
        classifications_data = [
            {'name': 'Furniture', 'icon': '🪑', 'description': 'Sofas, chairs, tables, and more'},
            {'name': 'Tiles', 'icon': '🧱', 'description': 'Floor and wall tiles'},
            {'name': 'Paints', 'icon': '🎨', 'description': 'Interior and exterior paints'},
            {'name': 'Ceiling & Gypsum', 'icon': '🏠', 'description': 'Ceiling materials and gypsum boards'},
            {'name': 'Lighting & Fixtures', 'icon': '💡', 'description': 'Lights, chandeliers, and fixtures'},
            {'name': 'Curtains & Carpets', 'icon': '🪟', 'description': 'Window treatments and floor coverings'},
            {'name': 'Doors & Windows', 'icon': '🚪', 'description': 'Doors, windows, and frames'},
            {'name': 'Outdoor & Garden', 'icon': '🌱', 'description': 'Garden supplies and outdoor furniture'},
            {'name': 'Bathroom & Kitchen', 'icon': '🛁', 'description': 'Fixtures and accessories'},
        ]

        for data in classifications_data:
            classification, created = Classification.objects.get_or_create(
                name=data['name'],
                defaults={
                    'icon': data['icon'],
                    'description': data['description']
                }
            )
            if created:
                self.stdout.write(f'Created classification: {classification.name}')

        # Create Shops
        shops_data = [
            {'name': 'Modern Furniture Store', 'classification': 'Furniture', 'description': 'Contemporary furniture for modern homes', 'address': '123 Main St, City Center', 'phone': '+1-555-0123'},
            {'name': 'Tile Masters', 'classification': 'Tiles', 'description': 'Premium tiles for floors and walls', 'address': '456 Oak Ave, Downtown', 'phone': '+1-555-0456'},
            {'name': 'Color World Paints', 'classification': 'Paints', 'description': 'High-quality paints and coatings', 'address': '789 Pine St, Midtown', 'phone': '+1-555-0789'},
            {'name': 'Bright Lights Co.', 'classification': 'Lighting & Fixtures', 'description': 'Modern lighting solutions', 'address': '321 Elm St, Uptown', 'phone': '+1-555-0321'},
            {'name': 'Home Textiles Plus', 'classification': 'Curtains & Carpets', 'description': 'Beautiful curtains and carpets', 'address': '654 Maple Dr, Suburb', 'phone': '+1-555-0654'},
        ]

        for data in shops_data:
            classification = Classification.objects.get(name=data['classification'])
            shop, created = Shop.objects.get_or_create(
                name=data['name'],
                defaults={
                    'classification': classification,
                    'description': data['description'],
                    'address': data['address'],
                    'phone': data['phone']
                }
            )
            if created:
                self.stdout.write(f'Created shop: {shop.name}')

        # Create Products
        products_data = [
            # Furniture
            {'name': 'Modern Sofa Set', 'shop': 'Modern Furniture Store', 'price': 1200.00, 'description': 'Comfortable 3-seater sofa with matching armchairs'},
            {'name': 'Dining Table', 'shop': 'Modern Furniture Store', 'price': 800.00, 'description': 'Solid wood dining table for 6 people'},
            {'name': 'Office Chair', 'shop': 'Modern Furniture Store', 'price': 250.00, 'description': 'Ergonomic office chair with lumbar support'},
            
            # Tiles
            {'name': 'Ceramic Floor Tiles', 'shop': 'Tile Masters', 'price': 45.00, 'description': 'High-quality ceramic tiles, 12x12 inches'},
            {'name': 'Marble Wall Tiles', 'shop': 'Tile Masters', 'price': 85.00, 'description': 'Premium marble tiles for bathroom walls'},
            {'name': 'Porcelain Tiles', 'shop': 'Tile Masters', 'price': 65.00, 'description': 'Durable porcelain tiles for high-traffic areas'},
            
            # Paints
            {'name': 'Interior Wall Paint', 'shop': 'Color World Paints', 'price': 35.00, 'description': 'Premium interior paint, 1 gallon'},
            {'name': 'Exterior Paint', 'shop': 'Color World Paints', 'price': 45.00, 'description': 'Weather-resistant exterior paint'},
            {'name': 'Primer', 'shop': 'Color World Paints', 'price': 25.00, 'description': 'High-quality primer for better paint adhesion'},
            
            # Lighting
            {'name': 'LED Chandelier', 'shop': 'Bright Lights Co.', 'price': 300.00, 'description': 'Modern LED chandelier with dimmer'},
            {'name': 'Table Lamp', 'shop': 'Bright Lights Co.', 'price': 75.00, 'description': 'Stylish table lamp with USB charging port'},
            {'name': 'Ceiling Fan', 'shop': 'Bright Lights Co.', 'price': 150.00, 'description': 'Energy-efficient ceiling fan with light'},
            
            # Textiles
            {'name': 'Blackout Curtains', 'shop': 'Home Textiles Plus', 'price': 120.00, 'description': 'Thermal blackout curtains, set of 2'},
            {'name': 'Area Rug', 'shop': 'Home Textiles Plus', 'price': 200.00, 'description': 'Hand-woven area rug, 8x10 feet'},
            {'name': 'Throw Pillows', 'shop': 'Home Textiles Plus', 'price': 35.00, 'description': 'Decorative throw pillows, set of 4'},
        ]

        for data in products_data:
            shop = Shop.objects.get(name=data['shop'])
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'shop': shop,
                    'price': data['price'],
                    'description': data['description']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create Budget Estimates
        estimates_data = [
            {'classification': 'Furniture', 'min_price': 500.00, 'max_price': 3000.00, 'average_price': 1500.00},
            {'classification': 'Tiles', 'min_price': 200.00, 'max_price': 1500.00, 'average_price': 800.00},
            {'classification': 'Paints', 'min_price': 100.00, 'max_price': 800.00, 'average_price': 400.00},
            {'classification': 'Lighting & Fixtures', 'min_price': 150.00, 'max_price': 1200.00, 'average_price': 600.00},
            {'classification': 'Curtains & Carpets', 'min_price': 100.00, 'max_price': 1000.00, 'average_price': 500.00},
        ]

        for data in estimates_data:
            classification = Classification.objects.get(name=data['classification'])
            estimate, created = BudgetEstimate.objects.get_or_create(
                classification=classification,
                defaults={
                    'min_price': data['min_price'],
                    'max_price': data['max_price'],
                    'average_price': data['average_price']
                }
            )
            if created:
                self.stdout.write(f'Created budget estimate for: {classification.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )





