import sys, os
import django
import __builtin__


def setup():
    sys.path.append('.')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nervous.settings')
    django.setup()
    import database.models as models
    for klass in ['Admin', 'OfficialAccount', 'Application', 'Article', 'Message', 'Student']:
        setattr(__builtin__, klass, getattr(models, klass).objects)
    for enum in ['SortOrder', 'SortBy', 'MessageCategory']:
        setattr(__builtin__, enum, getattr(models, enum))


if __name__ == '__main__':
    setup()
