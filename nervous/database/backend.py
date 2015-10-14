from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import setup_db
from trans import *

setup_db.setup()


# Applications

def trans_application(a):
    return map(application_to_dict, a)


def get_applications():
    return trans_application(Application.all())


def get_applications_by_status(status):
    return trans_application(Application.filter(status__exact=status))


def get_pending_applications():
    return get_applications_by_status('pending')


def get_applications_by_user(username):
    return trans_application(Application.filter(user_submit__exact=username))


def add_application(app):
    pass


# Official Accounts

def trans_account(a):
    return map(official_account_to_dict, a)


def get_official_accounts():
    return trans_account(OfficialAccount.all())


# Admins

def add_admin(username, md5_password):
    try:
        Admin.create(username=username, password=md5_password)
        return True
    except IntegrityError:
        return False


def del_admin(username):
    try:
        admin = Admin.get(username=username)
        admin.delete()
        return True
    except ObjectDoesNotExist:
        return False


def get_admins():
    return Admin.all()


# Articles

def trans_article(a):
    return map(article_to_dict, a)


def get_articles():
    return trans_article(Article.all())
