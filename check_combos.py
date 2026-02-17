import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveCafe.settings')
django.setup()

from cafe.models import MenuItem

combos = MenuItem.objects.filter(category='COMBO', menu_section='OTHER')
print(f"Total Combos: {combos.count()}")
for c in combos:
    print(f"- {c.name}: {c.description}")
