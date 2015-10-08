import sys, os
import django
import __builtin__

def setup():
    sys.path.append('.')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nervous.settings')
    django.setup()
    from database.models import Admin, OfficialAccount, Application
    __builtin__.Admin = Admin
    __builtin__.OfficialAccount = OfficialAccount
    __builtin__.Application = Application

setup()
