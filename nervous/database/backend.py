from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import setup_db

setup_db.setup()


# Applications

def get_applications():
    return Application.all()


def get_applications_by_status(status):
    return Application.filter(status__exact=status)


def get_pending_applications():
    return get_applications_by_status('pending')


def get_applications_by_user(username):
    return Application.filter(user_submit__exact=username)


def add_application(app):
    print app
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
        account = OfficialAccount.get(pk=app['account_id'])
        application = Application.get(pk=account)
        application.status = app['status']
        application.save()
    except ObjectDoesNotExist:
        return False


# Official Accounts

def get_official_accounts():
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

def get_articles():
    return Article.all()


def add_article(dic):
    try:
        art = Article.get(url__exact=dic['url'])
    except ObjectDoesNotExist:
        # TODO: use wx_id instead of name
        acc_name = dic['name']
        try:
            acc = OfficialAccount.get(name__exact=acc_name)
        except ObjectDoesNotExist:
            acc = OfficialAccount.create(name=acc_name, description=acc_name)
        art = Article.model()
        art.official_account_id = acc.id
        for attr in ['title', 'description', 'avatar_url', 'url']:
            setattr(art, attr, dic[attr])
        art.save()
    ArticleDailyRecord.create(
        article = art,
        likes = dic['likes'],
        views = dic['views'],
        update_time = dic['update_time']
    )


def get_articles_by_official_account_id(id):
    return Article.filter(official_account_id__exact=id)
