from main_app.models import Classification, Shop

def create_shops():
    shops_data = [
        {'name': 'Modern Furniture Store', 'classification': 'Furniture', 'description': 'High-quality modern furniture for your home'},
        {'name': 'Elegant Tiles', 'classification': 'Tiles', 'description': 'Premium tiles for floors and walls'},
        {'name': 'ColorMaster Paints', 'classification': 'Paints', 'description': 'Wide range of paint colors and finishes'},
        {'name': 'Ceiling Experts', 'classification': 'Ceiling & Gypsum', 'description': 'Professional ceiling and gypsum solutions'},
        {'name': 'Bright Lighting', 'classification': 'Lighting & Fixtures', 'description': 'Modern lighting solutions for every room'},
        {'name': 'Soft Furnishings', 'classification': 'Curtains & Carpets', 'description': 'Quality curtains and carpets for your home'},
        {'name': 'Door & Window World', 'classification': 'Doors & Windows', 'description': 'Stylish doors and windows for your home'},
        {'name': 'Garden Center', 'classification': 'Outdoor & Garden', 'description': 'Everything you need for your garden'},
        {'name': 'Kitchen & Bath Solutions', 'classification': 'Bathroom & Kitchen', 'description': 'Complete solutions for kitchens and bathrooms'}
    ]
    
    created_shops = []
    
    for shop_data in shops_data:
        try:
            classification = Classification.objects.get(name=shop_data['classification'])
            shop = Shop.objects.create(
                name=shop_data['name'],
                classification=classification,
                description=shop_data['description'],
                address='123 Main St',
                phone='555-123-4567',
                email=f'info@{shop_data["name"].lower().replace(" ", "")}.com'
            )
            created_shops.append(f'{shop.name} - {shop.classification.name}')
        except Exception as e:
            print(f'Error creating shop for {shop_data["classification"]}: {str(e)}')
    
    print('\nCreated Shops:\n' + '\n'.join(created_shops))

if __name__ == '__main__':
    create_shops()