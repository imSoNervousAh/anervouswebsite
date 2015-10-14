import sys, os
import django
import __builtin__


def setup():
    sys.path.append('.')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nervous.settings')
    django.setup()
    from database.models import Admin, OfficialAccount, Application, Article
    __builtin__.Admin = Admin.objects
    __builtin__.OfficialAccount = OfficialAccount.objects
    __builtin__.Application = Application.objects
    __builtin__.Article = Article.objects


if (__name__ == '__main__'):
    setup()
