import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multi_vendor_ecommerce.settings")

django.setup()

from django.core.management import call_command

call_command('loaddata', 'data.json')