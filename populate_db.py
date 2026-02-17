from django.core.files import File
from cafe.models import MenuItem, FranchisePackage
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()


def add_item(name, description, price, image_name, category='DRINK', season='ALL', is_special=False, is_seasonal=False, temp_type='COLD', spice_level=0, is_vegan=False, is_gluten_free=False):
    # Try .png first, then .jpg
    image_path_png = os.path.join('media', 'drinks', f'{image_name}.png')
    image_path_jpg = os.path.join('media', 'drinks', f'{image_name}.jpg')

    if os.path.exists(image_path_png):
        image_path = image_path_png
        ext = '.png'
    elif os.path.exists(image_path_jpg):
        image_path = image_path_jpg
        ext = '.jpg'
    else:
        image_path = None
        ext = None

    # Check if item already exists
    item, created = MenuItem.objects.get_or_create(
        name=name,
        defaults={
            'description': description,
            'price': price,
            'category': category,
            'season': season,
            'temp_type': temp_type,
            'is_special': is_special,
            'is_seasonal': is_seasonal,
            'spice_level': spice_level,
            'is_vegan': is_vegan,
            'is_gluten_free': is_gluten_free,
        }
    )

    if not created:
        item.category = category
        item.season = season
        item.temp_type = temp_type
        item.is_special = is_special
        item.is_seasonal = is_seasonal
        item.spice_level = spice_level
        item.is_vegan = is_vegan
        item.is_gluten_free = is_gluten_free
        item.save()

    # Attach the image if it exists
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            item.image.save(f'{image_name}{ext}', File(f), save=True)
    return item


def add_franchise_package(name, location_type, investment_range, description, setup_time, image_name):
    image_path = os.path.join('media', 'drinks', f'{image_name}.png')
    pkg, created = FranchisePackage.objects.get_or_create(
        name=name,
        defaults={
            'location_type': location_type,
            'investment_range': investment_range,
            'description': description,
            'setup_time': setup_time
        }
    )
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            pkg.image.save(f'{image_name}.png', File(f), save=True)
    return pkg


def populate():
    print("Populating database...")

    items = [
        # Regular Drinks (Cold)
        {'name': 'Iced Cappuccino', 'description': 'Frothy espresso chilled with milk.',
            'price': 250.00, 'image_name': 'iced_cappuccino', 'category': 'DRINK', 'temp_type': 'COLD'},
        {'name': 'Iced Espresso', 'description': 'Pure espresso over ice.', 'price': 180.00,
            'image_name': 'iced_espresso', 'category': 'DRINK', 'temp_type': 'COLD'},
        {'name': 'Iced Latte', 'description': 'Creamy espresso and cold milk.', 'price': 220.00,
            'image_name': 'iced_latte', 'category': 'DRINK', 'temp_type': 'COLD'},

        # Smoothies
        {'name': 'Very Berry', 'description': 'A burst of fresh berries blended to perfection.',
            'price': 280.00, 'image_name': 'very_berry_smoothie', 'category': 'SMOOTHIE', 'temp_type': 'COLD'},
        {'name': 'Mango Paradise', 'description': 'Tropical mango bliss in a glass.', 'price': 260.00,
            'image_name': 'mango_paradise_smoothie', 'category': 'SMOOTHIE', 'temp_type': 'COLD'},
        {'name': 'Kiwi Berry', 'description': 'Zesty kiwi and sweet berries fusion.', 'price': 270.00,
            'image_name': 'kiwi_berry_smoothie', 'category': 'SMOOTHIE', 'temp_type': 'COLD'},
        {'name': 'Chocolate Banana Smoothie', 'description': 'Rich chocolate meets creamy banana.',
            'price': 290.00, 'image_name': 'chocolate_banana_smoothie', 'category': 'SMOOTHIE', 'temp_type': 'COLD'},
        {'name': 'Chocolate Peanut Butter Banana', 'description': 'The ultimate protein-packed indulgence.',
            'price': 320.00, 'image_name': 'choco_pb_banana_smoothie', 'category': 'SMOOTHIE', 'temp_type': 'COLD'},

        {'name': 'Vanilla Reef Latte', 'description': 'Smooth vanilla and coastal espresso.',
            'price': 320.00, 'image_name': 'vanilla_reef_latte', 'category': 'DRINK', 'temp_type': 'COLD'},
        {'name': 'Sea Salt Caramel Cold Brew', 'description': '24-hour cold brew with caramel foam.',
            'price': 600.00, 'image_name': 'sea_salt_caramel', 'is_special': True, 'temp_type': 'COLD'},
        {'name': 'Blueberry Monsoon', 'description': 'Sparkling blueberry lemonade.', 'price': 450.00,
            'image_name': 'blueberry_monsoon', 'is_special': True, 'temp_type': 'COLD'},

        # Summer Specials (Mostly Cold)
        {'name': 'Iced Berry Fizz', 'description': 'Mixed berries with lime and fizz.', 'price': 380.00,
            'image_name': 'berry_fizz', 'category': 'DRINK', 'season': 'SUMMER', 'is_seasonal': True, 'temp_type': 'COLD'},

        # Monsoon Specials
        {'name': 'Cutting Chai', 'description': 'Strong ginger and cardamom tea.', 'price': 120.00,
            'image_name': 'cutting_chai', 'category': 'DRINK', 'season': 'MONSOON', 'is_seasonal': True, 'temp_type': 'HOT'},
        {'name': 'Corn Fritters', 'description': 'Crispy corn snacks perfect for rain.', 'price': 280.00,
            'image_name': 'corn_fritters', 'category': 'SNACK', 'season': 'MONSOON', 'is_seasonal': True, 'temp_type': 'NA'},

        # Winter Specials
        {'name': 'Spiced Hot Cocoa', 'description': 'Rich dark chocolate with cinnamon.', 'price': 420.00,
            'image_name': 'hot_cocoa', 'category': 'DRINK', 'season': 'WINTER', 'is_seasonal': True, 'temp_type': 'HOT'},
        {'name': 'Pumpkin Ginger Latte', 'description': 'Warming spiced pumpkin latte.', 'price': 480.00,
            'image_name': 'pumpkin_latte', 'category': 'DRINK', 'season': 'WINTER', 'is_seasonal': True, 'temp_type': 'HOT'},


        # Fresh Fruit Juices
        {'name': 'Watermelon Chill', 'description': 'Refreshing fresh watermelon juice with a hint of mint.',
            'price': 180.00, 'image_name': 'watermelon_chill', 'category': 'DRINK', 'temp_type': 'COLD', 'is_vegan': True},

        # Indian Starters (The Wave Fusion)
        {'name': 'Tandoori Prawns', 'description': 'Jumbo prawns marinated in coastal spices, clay-oven roasted.',
            'price': 550.00, 'image_name': 'tandoori_prawns', 'category': 'STARTER', 'spice_level': 3, 'is_gluten_free': True},
        {'name': 'Paneer Tacos', 'description': 'Fusion tacos with paneer tikka, spicy salsa, and mint chutney.',
            'price': 320.00, 'image_name': 'paneer_tacos', 'category': 'STARTER', 'spice_level': 1},
        {'name': 'Masala Calamari', 'description': 'Crispy squid rings tossed in a fiery south Indian spice mix.',
            'price': 480.00, 'image_name': 'masala_calamari', 'category': 'STARTER', 'spice_level': 2, 'is_gluten_free': True},
        {'name': 'Saffron Sliders', 'description': 'Mini chicken burgers with saffron garlic aioli.',
            'price': 380.00, 'image_name': 'saffron_sliders', 'category': 'STARTER', 'spice_level': 0},
        {'name': 'Gunpowder Wings', 'description': 'Crispy chicken wings glazed with spicy podi-infused butter.',
            'price': 420.00, 'image_name': 'gunpowder_wings', 'category': 'STARTER', 'spice_level': 3, 'is_gluten_free': True},
    ]

    # Remove old items if they exist
    MenuItem.objects.filter(name__in=['Papaya Nectar', 'Papaya Juice',
                            'Kiwi Spark', 'Mango Sparkle', 'Tropical Sunrise']).delete()

    # Process and add all items
    for item_data in items:
        add_item(**item_data)
    print(f"Processed {len(items)} menu items.")

    franchise_packages = [
        {
            'name': 'Sandy Shore Kiosk',
            'location_type': 'BEACH',
            'investment_range': '5 - 8 Lakhs',
            'description': 'A vibrant, compact kiosk perfect for high-traffic beach promenades.',
            'setup_time': '3-4 weeks',
            'image_name': 'beach_cart'
        },
        {
            'name': 'High-Tide Highway Hub',
            'location_type': 'HIGHWAY',
            'investment_range': '10 - 15 Lakhs',
            'description': 'A robust container-style cafe designed for highway pitstops.',
            'setup_time': '6-8 weeks',
            'image_name': 'highway_hub'
        },
        {
            'name': 'Campus Wave Cart',
            'location_type': 'COLLEGE',
            'investment_range': '3 - 5 Lakhs',
            'description': 'A mobile cart optimized for university campuses.',
            'setup_time': '2 weeks',
            'image_name': 'campus_cart'
        },
        {
            'name': 'Metro Mall Pod',
            'location_type': 'MALL',
            'investment_range': '12 - 18 Lakhs',
            'description': 'A premium, sleek pod format for upscale shopping malls.',
            'setup_time': '5-6 weeks',
            'image_name': 'mall_kiosk'
        }
    ]

    for pkg_data in franchise_packages:
        add_franchise_package(**pkg_data)
    print(f"Processed {len(franchise_packages)} franchise packages.")


if __name__ == '__main__':
    populate()
