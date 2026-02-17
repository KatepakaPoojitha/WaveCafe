
import os
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()

from cafe.models import MenuItem

def add_high_margin_item(name, description, price, image_name, category='STARTER', menu_section='OTHER', is_seasonal=False, spice_level=0, is_vegan=False, is_gluten_free=False, temp_type='COLD'):
    image_path = os.path.join('media', 'drinks', f'{image_name}.png')
    
    item, created = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'description': description,
            'price': price,
            'category': category,
            'menu_section': menu_section,
            'is_seasonal': is_seasonal,
            'spice_level': spice_level,
            'is_vegan': is_vegan,
            'is_gluten_free': is_gluten_free,
            'temp_type': temp_type,
        }
    )
    
    if not created:
        item.description = description
        item.price = price
        item.category = category
        item.menu_section = menu_section
        item.is_seasonal = is_seasonal
        item.spice_level = spice_level
        item.is_vegan = is_vegan
        item.is_gluten_free = is_gluten_free
        item.temp_type = temp_type
        item.save()

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            item.image.save(f'{image_name}.png', File(f), save=True)
    return item

def populate_high_margin_items():
    items = [
        # Loaded Fries (High Margin, Low Cost)
        {
            "name": "Peri-Peri Cheesy Fries",
            "description": "Crispy fries tossed in peri-peri spice, topped with liquid cheese and jalapeños.",
            "price": 180.00,
            "category": "STARTER",
            "menu_section": "LOADED_FRIES",
            "image_name": "peri_peri_fries",
            "spice_level": 2,
            "is_gluten_free": True
        },
        {
            "name": "BBQ Chicken Fries",
            "description": "Fries loaded with shredded BBQ chicken, caramelized onions, and smoky mayo.",
            "price": 220.00,
            "category": "STARTER",
            "menu_section": "LOADED_FRIES",
            "image_name": "bbq_chicken_fries",
            "spice_level": 1
        },

        # Fusion Chaat
        {
            "name": "Nachos Bhel",
            "description": "Mexican-Indian fusion with tortilla chips, salsa, tamarind chutney, and sev.",
            "price": 160.00,
            "category": "STARTER",
            "menu_section": "FUSION_CHAAT",
            "image_name": "nachos",
            "spice_level": 2,
            "is_vegan": True
        },
        {
            "name": "Chicken Tikka Sev Puri",
            "description": "Crispy puris topped with minced chicken tikka, mint chutney, and pomegranate.",
            "price": 200.00,
            "category": "STARTER",
            "menu_section": "FUSION_CHAAT",
            "image_name": "nachos",
            "spice_level": 2
        },

        # Flavored Lemonades
        {
            "name": "Blue Lagoon Lemonade",
            "description": "Sparkling blue curacao lemonade with fresh mint and lemon slices.",
            "price": 140.00,
            "category": "DRINK",
            "menu_section": "OTHER",
            "temp_type": "COLD",
            "image_name": "lemonade",
            "is_vegan": True,
            "is_gluten_free": True
        },
        {
            "name": "Spiced Jamun Fizz",
            "description": "Real jamun pulp shaken with black salt, cumin, and soda.",
            "price": 150.00,
            "category": "DRINK",
            "menu_section": "OTHER",
            "temp_type": "COLD",
            "image_name": "lemonade",
            "is_seasonal": True,
            "season": "MONSOON",
            "spice_level": 1,
            "is_vegan": True,
            "is_gluten_free": True
        },

        # Combos
        {
            "name": "Sip & Snack Combo",
            "description": "Any Loaded Fries + Blue Lagoon Lemonade.",
            "price": 280.00,
            "category": "COMBO",
            "menu_section": "OTHER",
            "image_name": "combo_meal",
            "spice_level": 2,
            "is_vegan": True
        },
        {
            "name": "Date Night Combo",
            "description": "2 Flavoured Lemonades + 1 Fusion Chaat + 1 Fries.",
            "price": 499.00,
            "category": "COMBO",
            "menu_section": "OTHER",
            "image_name": "combo_meal",
            "spice_level": 1,
            "is_vegan": True
        },
        {
            "name": "Classic Shawarma Combo",
            "description": "Chicken Shawarma Roll + Medium Fries + Coke. The perfect solo meal.",
            "price": 250.00,
            "category": "COMBO",
            "menu_section": "OTHER",
            "image_name": "combo_meal",
            "spice_level": 1
        },
        {
            "name": "Student Saver",
            "description": "Masala Maggi + Iced Lemon Tea. heavy discount for students.",
            "price": 120.00,
            "category": "COMBO",
            "menu_section": "OTHER",
            "image_name": "combo_meal",
            "spice_level": 1,
            "is_vegan": True
        },

        # Family & Party Packs
        {
            "name": "Weekend Binge Box",
            "description": "2 Shawarma Rolls + 1 Peri-Peri Fries + 2 Cold Coffees.",
            "price": 550.00,
            "category": "SNACK",
            "menu_section": "FAMILY_BOX",
            "image_name": "party_pack",
            "spice_level": 1
        },
        {
            "name": "Match Day Platter",
            "description": "6 BBQ Wings + 1 Loaded Fries + Nachos Bhel + 4 Cokes.",
            "price": 999.00,
            "category": "SNACK",
            "menu_section": "PARTY_PACK",
            "image_name": "party_pack",
            "spice_level": 2
        }
    ]

    for item_data in items:
        add_high_margin_item(**item_data)
        print(f"Processed: {item_data['name']}")

if __name__ == '__main__':
    populate_high_margin_items()
