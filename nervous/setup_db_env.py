import sys, os
import django

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nervous.settings')

django.setup()

from database.models import Admin, OfficialAccount, Application
