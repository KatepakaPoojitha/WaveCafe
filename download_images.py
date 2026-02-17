import os
import requests

def download_image(url, filename):
    try:
        # User-agent header can help avoid some 403 blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, stream=True, timeout=15, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {url}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    media_dir = os.path.join('media', 'drinks')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    # Beautiful, high-quality professional photography URLs
    images = {
        'about_cafe.jpg': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=1200',
        'hero_bg.jpg': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=1600',
        'golden_latte.png': 'https://images.unsplash.com/photo-1614707267537-b85aaf00c4b7?q=80&w=800',
        'sea_salt_caramel.png': 'https://images.unsplash.com/photo-1559496417-e7f25cb247f3?q=80&w=800', # Caramel coffee
        'blueberry_monsoon.png': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=800', # Blueberry bubbly
        'iced_cappuccino.png': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?q=80&w=800',
        'iced_espresso.png': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?q=80&w=800',
        'iced_latte.png': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?q=80&w=800',
        'vanilla_reef_latte.png': 'https://images.unsplash.com/photo-1506458268469-52d12c90df1d?q=80&w=800',
        'watermelon_chill.png': 'https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?q=80&w=800',
        # Smoothies
        'very_berry_smoothie.png': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?q=80&w=800',
        'mango_paradise_smoothie.png': 'https://images.unsplash.com/photo-1490239632855-f48d23a71387?q=80&w=800',
        'kiwi_berry_smoothie.png': 'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?q=80&w=800',
        'chocolate_banana_smoothie.png': 'https://images.unsplash.com/photo-1577805947697-89e18249d767?q=80&w=800',
        'choco_pb_banana_smoothie.png': 'https://images.unsplash.com/photo-1610970882739-449558711972?q=80&w=800',
        'irish_coffee.png': 'https://images.unsplash.com/photo-1504933350103-e840ede978d4?q=80&w=800',
        # Indian Starters
        'tandoori_prawns.png': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=800',
        'paneer_tacos.png': 'https://images.unsplash.com/photo-1585238342024-78d387f4a707?q=80&w=800',
        'masala_calamari.png': 'https://images.unsplash.com/photo-1590593162201-f67611a18b87?q=80&w=800',
        'saffron_sliders.png': 'https://images.unsplash.com/photo-1550547660-d9450f859349?q=80&w=800',
        'gunpowder_wings.png': 'https://images.unsplash.com/photo-1527477396000-e27163b481c2?q=80&w=800',
        # New Chicken items
        'chicken_shawarma_roll.png': 'https://images.unsplash.com/photo-1662116765994-1e4200c4066a?q=80&w=800',
        'shawarma_platter.png': 'https://images.unsplash.com/photo-1561651823-34feb02250e4?q=80&w=800',
        'pepper_grilled_chicken.png': 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?q=80&w=800',
        'peri_peri_grilled.png': 'https://images.unsplash.com/photo-1596450514735-2440380fe807?q=80&w=800',
        'bbq_wings.png': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?q=80&w=800',
        'tandoori_chicken.png': 'https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?q=80&w=800',
        'chicken_tikka.png': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=800',
        # New Veg items
        'corn_fritters.png': 'https://images.unsplash.com/photo-1528279027-68f0d7fce9f1?q=80&w=800',
        'paneer_tikka.png': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?q=80&w=800',
        'cocktail_samosas.png': 'https://images.unsplash.com/photo-1601050638917-3d8bc33ef8bc?q=80&w=800',
        # High Margin & Combo items
        'peri_peri_fries.png': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?q=80&w=800',
        'bbq_chicken_fries.png': 'https://images.unsplash.com/photo-1585109649139-366815a0d713?q=80&w=800',
        'nachos.png': 'https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?q=80&w=800',
        'lemonade.png': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=800',
        'combo_meal.png': 'https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?q=80&w=800',
        'party_pack.png': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800',
        'cutting_chai.png': 'https://images.unsplash.com/photo-1594631252845-29fc45863d0c?q=80&w=800',
        'corn_fritters_monsoon.png': 'https://images.unsplash.com/photo-1528279027-68f0d7fce9f1?q=80&w=800',
        
        # Missing Items from 404s and Logs
        'corn_balls.jpg': 'https://images.unsplash.com/photo-1541529086526-db283c563270?q=80&w=800', # Fried balls
        'party_pack.jpg': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800', # Pizza/party food
        'peri_fries.jpg': 'https://images.unsplash.com/photo-1630384066252-11e1ed8fd571?q=80&w=800', 
        'mexican_fries.jpg': 'https://images.unsplash.com/photo-1518013391915-e443bdba0a7d?q=80&w=800', 
        'family_box.jpg': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800', 
        'pink_lemonade.jpg': 'https://images.unsplash.com/photo-1536935338218-c918fc0966a3?q=80&w=800',
        'combo_sip_snack.jpg': 'https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?q=80&w=800',
        'combo_date.jpg': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?q=80&w=800',
        'combo.jpg': 'https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?q=80&w=800',
        'combo_student.jpg': 'https://images.unsplash.com/photo-1593179241557-bce1eb92e47e?q=80&w=800',
        'party.jpg': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800',
        'deal_01.jpg': 'https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?q=80&w=800',
        'deal_02.jpg': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800',
        'deal_03.jpg': 'https://images.unsplash.com/photo-1550547660-d9450f859349?q=80&w=800',
        'deal_04.jpg': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800',
        'deal_05.jpg': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=800',
        'deal_06.jpg': 'https://images.unsplash.com/photo-1574484284002-952d92456975?q=80&w=800',
        'deal_07.jpg': 'https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800',
    }

    for filename, url in images.items():
        path = os.path.join(media_dir, filename)
        # Force refresh all images to ensure we get the high-quality ones
        download_image(url, path)

if __name__ == '__main__':
    main()
