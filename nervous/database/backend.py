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
    app = app.dict()
    name, description = app['name'], app['description']
    for k in ['name', 'description', 'csrfmiddlewaretoken']:
        del app[k]
    try:
        OfficialAccount.get(name__exact=name)
        print "Error: account already exists."
    except ObjectDoesNotExist:
        account = OfficialAccount.create(name=name, description=description)
        app['official_account'] = account
        app['status'] = 'pending'
        Application.create(**app)
        return True


def modify_application(app):
    app = app.dict()
    print app
    try:
        print app['account_name']
        account = OfficialAccount.get(name__exact=app['account_name'])
        print account
        application = Application.get(pk=account)
        print application
        application.status = app['status']
        application.save()
    except ObjectDoesNotExist:
        return False


# Official Accounts

def trans_account(a):
    return map(official_account_to_dict, a)


def get_official_accounts():
    # return trans_account(OfficialAccount.all())
    return OfficialAccount.all()

def get_official_account_by_id(id):
    return OfficialAccount.get(pk=id)


# Admins

def add_admin(username, md5_password, description):
    try:
        Admin.create(username=username, password=md5_password, description=description)
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

def check_admin(username, password):
    try:
        admin = Admin.get(username=username)
        return admin.password == password
    except ObjectDoesNotExist:
        return False


# Articles

def trans_article(a):
    return map(article_to_dict, a)


def get_articles():
    return trans_article(Article.all())


def add_article(dic):
    pass


def get_articles_by_official_account_id(id):
    return trans_article(Article.filter(official_account_id__exact=id))

