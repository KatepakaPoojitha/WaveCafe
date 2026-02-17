
import os
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()

from cafe.models import MenuItem

def add_combo_item(name, description, price, image_name, category='COMBO', menu_section='OTHER', is_special=False):
    image_path = os.path.join('media', 'drinks', f'{image_name}.png')
    
    item, created = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'description': description,
            'price': price,
            'category': category,
            'menu_section': menu_section,
            'is_special': is_special,
        }
    )
    
    if not created:
        item.description = description
        item.price = price
        item.is_special = is_special
        item.save()

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            item.image.save(f'{image_name}.png', File(f), save=True)
    return item

def populate_combos():
    items = [
        # --- New 7 Deals ---
        {
            "name": "Deal #01",
            "description": "Beef Burger + Chicken Roll + Soft Drink 345ml",
            "price": 520.00,
            "category": "COMBO",
            "image_name": "combo_meal"
        },
        {
            "name": "Deal #02",
            "description": "Chicken Burger + Beef Roll + Soft Drink 345ml",
            "price": 520.00,
            "category": "COMBO",
            "image_name": "combo_meal"
        },
        {
            "name": "Deal #03",
            "description": "Zinger Burger + Chicken Roll + Soft Drink 345ml",
            "price": 600.00,
            "category": "COMBO",
            "is_special": True,
            "image_name": "combo_meal"
        },
        {
            "name": "Deal #04",
            "description": "Masala Broast + Chicken Roll + Soft Drink 345ml",
            "price": 610.00,
            "category": "COMBO",
            "image_name": "combo_meal"
        },
        {
            "name": "Deal #05",
            "description": "Jumbo Zinger Burger + Chicken Roll + Beef Roll + Soft Drink 500ml",
            "price": 960.00,
            "category": "COMBO",
            "is_special": True,
            "image_name": "combo_meal"
        },
        {
            "name": "Deal #06",
            "description": "Chicken Tikka + Singaporian Rice + Paratha + Soft Drink 500ml",
            "price": 930.00,
            "category": "COMBO",
            "image_name": "combo_meal"
        },
        {
            "name": "Deal #07",
            "description": "Chicken Tikka + Beef Boti + 02 Paratha + Soft Drink 500ml",
            "price": 990.00,
            "category": "COMBO",
            "is_special": True,
            "image_name": "combo_meal"
        }
    ]

    for item_data in items:
        add_combo_item(**item_data)
        print(f"Processed Combo: {item_data['name']}")

if __name__ == '__main__':
    populate_combos()
