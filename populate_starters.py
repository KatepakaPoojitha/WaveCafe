
import os
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()

from cafe.models import MenuItem

def add_starter_item(name, description, price, image_name, category='STARTER', temp_type='HOT', spice_level=0, is_vegan=False, is_gluten_free=False):
    image_path = os.path.join('media', 'drinks', f'{image_name}.png')
    
    item, created = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'description': description,
            'price': price,
            'category': category,
            'temp_type': temp_type,
            'spice_level': spice_level,
            'is_vegan': is_vegan,
            'is_gluten_free': is_gluten_free,
            'menu_section': 'VEG_STARTERS'
        }
    )
    
    if not created:
        item.description = description
        item.price = price
        item.temp_type = temp_type
        item.spice_level = spice_level
        item.is_vegan = is_vegan
        item.is_gluten_free = is_gluten_free
        item.menu_section = 'VEG_STARTERS'
        item.save()

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            item.image.save(f'{image_name}.png', File(f), save=True)
    return item

def add_starters():
    # Clear existing starters to avoid duplicates if re-running
    # MenuItem.objects.filter(category='STARTER').delete() 
    # print("Cleared existing starters.")

    starters = [
        {
            "name": "Spicy Corn Fritters",
            "description": "Golden, crispy corn kernels tossed with fresh herbs and spices, served with zesty mint chutney.",
            "price": 180.00,
            "image_name": "corn_fritters",
            "category": "STARTER",
            "temp_type": "HOT",
            "spice_level": 2,
            "is_vegan": True,
            "is_gluten_free": True
        },
        {
            "name": "Paneer Tikka Bites",
            "description": "Grilled cottage cheese cubes marinated in aromatic spices, skewered with bell peppers and onions.",
            "price": 240.00,
            "image_name": "paneer_tikka",
            "category": "STARTER",
            "temp_type": "HOT",
            "spice_level": 2,
            "is_vegan": False,
            "is_gluten_free": True
        },
        {
            "name": "Cocktail Samosas",
            "description": "Mini triangular pastries filled with spiced potatoes and peas, fried to golden perfection.",
            "price": 150.00,
            "image_name": "cocktail_samosas",
            "category": "STARTER",
            "temp_type": "HOT",
            "spice_level": 1,
            "is_vegan": True,
            "is_gluten_free": False
        }
    ]

    for item_data in starters:
        add_starter_item(**item_data)
        print(f"Processed Starter: {item_data['name']}")

if __name__ == '__main__':
    add_starters()
