import os
import shutil

def fix_media():
    drinks_dir = os.path.join('media', 'drinks')
    menu_dir = os.path.join('media', 'menu')
    
    if not os.path.exists(menu_dir):
        os.makedirs(menu_dir)
        
    # List of images to copy from drinks to menu
    images_to_fix = [
        'corn_balls.jpg',
        'party_pack.jpg',
        'peri_fries.jpg',
        'mexican_fries.jpg',
        'family_box.jpg',
        'pink_lemonade.jpg',
        'combo_sip_snack.jpg',
        'combo_date.jpg',
        'combo.jpg',
        'combo_student.jpg',
        'party.jpg',
        'deal_01.jpg',
        'deal_02.jpg',
        'deal_03.jpg',
        'deal_04.jpg',
        'deal_05.jpg',
        'deal_06.jpg',
        'deal_07.jpg',
    ]
    
    count = 0
    for img in images_to_fix:
        src = os.path.join(drinks_dir, img)
        dst = os.path.join(menu_dir, img)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Fixed: {img}")
            count += 1
        else:
            print(f"Warning: {img} not found in {drinks_dir}")
            
    print(f"Total images fixed: {count}")

if __name__ == '__main__':
    fix_media()
