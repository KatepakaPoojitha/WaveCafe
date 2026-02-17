
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()

from cafe.models import MenuItem

def check_starters():
    starters = MenuItem.objects.filter(category='STARTER')
    print(f"Found {starters.count()} starters.")
    for starter in starters:
        print(f"Name: {starter.name}")
        print(f"  Image Field: {starter.image}")
        if starter.image:
            print(f"  Image URL: {starter.image.url}")
            # Check if file exists
            file_path = os.path.join(settings.MEDIA_ROOT, str(starter.image))
            exists = os.path.exists(file_path)
            print(f"  File Exists: {exists}")
        else:
            print("  No image assigned.")

if __name__ == '__main__':
    check_starters()
