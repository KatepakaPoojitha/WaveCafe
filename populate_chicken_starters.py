
import os
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()

from cafe.models import MenuItem

def add_chicken_item(name, description, price, image_name, menu_section):
    image_path = os.path.join('media', 'drinks', f'{image_name}.png')
    
    item, created = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'description': description,
            'price': price,
            'category': 'STARTER',
            'menu_section': menu_section,
        }
    )
    
    if not created:
        item.description = description
        item.price = price
        item.menu_section = menu_section
        item.save()

    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            item.image.save(f'{image_name}.png', File(f), save=True)
    return item

def populate_chicken_starters():
    # 1. Update Existing Starters to 'VEG_STARTERS'
    veg_starters = MenuItem.objects.filter(category='STARTER').exclude(menu_section__in=['SHAWARMA_ROLL', 'SHAWARMA_PLATE', 'GRILLED_CHICKEN', 'BBQ_CHICKEN', 'TANDOORI_CHICKEN'])
    count = veg_starters.update(menu_section='VEG_STARTERS')
    print(f"Updated {count} existing starters to VEG_STARTERS section.")

    # 2. Add New Chicken Items
    chicken_items = [
        # Chicken Shawarma Roll
        {
            "name": "Classic Shawarma Roll",
            "description": "Juicy spice-rubbed chicken wrapped in soft rumali roti with garlic mayo.",
            "price": 120.00,
            "menu_section": "SHAWARMA_ROLL",
            "image_name": "shawarma_platter" # Using platter as fallback since roll failed
        },
        {
            "name": "Spicy Mexican Roll",
            "description": "Shawarma chicken with jalapenos, salsa lint, and spicy mayo.",
            "price": 150.00,
            "menu_section": "SHAWARMA_ROLL",
            "image_name": "shawarma_platter"
        },
        
        # Chicken Shawarma Plate
        {
            "name": "Shawarma Platter",
            "description": "Open plate serving of roasted chicken, salad, khubus, and hummus.",
            "price": 220.00,
            "menu_section": "SHAWARMA_PLATE",
            "image_name": "shawarma_platter"
        },
        
        # Grilled Chicken
        {
            "name": "Pepper Grilled Chicken",
            "description": "Quarter bird marinated in crushed black pepper and lime, grilled to perfection.",
            "price": 280.00,
            "menu_section": "GRILLED_CHICKEN",
            "image_name": "pepper_grilled_chicken"
        },
        {
            "name": "Peri Peri Grilled",
            "description": "Spicy African bird's eye chili marinade, smoky and charred.",
            "price": 300.00,
            "menu_section": "GRILLED_CHICKEN",
            "image_name": "peri_peri_grilled"
        },

        # Barbeque Chicken
        {
            "name": "Smoked BBQ Wings",
            "description": "6 pieces of wings glazed in our house special hickory smoked BBQ sauce.",
            "price": 240.00,
            "menu_section": "BBQ_CHICKEN",
            "image_name": "bbq_wings"
        },

        # Tandoori Chicken
        {
            "name": "Tandoori Chicken Half",
            "description": "Traditional clay oven roasted chicken succulent with yogurt and spices.",
            "price": 350.00,
            "menu_section": "TANDOORI_CHICKEN",
            "image_name": "tandoori_chicken"
        },
        {
            "name": "Chicken Tikka",
            "description": "Boneless chicken chunks marinated in spiced yogurt and grilled.",
            "price": 260.00,
            "menu_section": "TANDOORI_CHICKEN",
            "image_name": "chicken_tikka"
        }
    ]

    for item_data in chicken_items:
        add_chicken_item(**item_data)
        print(f"Processed: {item_data['name']}")

if __name__ == '__main__':
    populate_chicken_starters()
