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


# TODO: add wx_id
# TODO: unique wx_id validation
def add_application(app):
    name = app['name']
    description = app.get('description', name)
    try:
        OfficialAccount.get(name__exact=name)
        return False
    except ObjectDoesNotExist:
        application = Application.model()
        account = OfficialAccount.create(name=name, description=description)
        application.official_account = account
        application.status = 'pending'
        for attr in [
            'manager_name', 'manager_student_id',
            'manager_dept', 'manager_tel', 'manager_email',
            'user_submit']:
            val = app.get(attr, '')
            setattr(application, attr, val)
        try:
            application.save()
            return True
        except:
            return False


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


# Students

def set_student_information(student_id, real_name):
    try:
        student = Student.create(student_id=student_id)
    except IntegrityError:
        student = Student.get(pk=student_id)
    student.real_name = real_name
    student.save()


def check_student_information_filled(student_id):
    try:
        student = Student.get(pk=student_id)
    except ObjectDoesNotExist:
        student = Student.create(student_id=student_id)
    return student.information_filled()


# Articles

def get_articles(sortby=SortBy.Time, order=SortOrder.Descending, start_from=0, count=10, filter=None):
    articles = Article.all()
    articles_count = len(articles)
    filter = filter or {}
    official_account_id = filter.get('official_account_id', None)
    article_title_keyword = filter.get('article_title_keyword', None)
    if official_account_id:
        articles = articles.filter(official_account_id__exact=official_account_id)
    if article_title_keyword:
        articles = articles.filter(title__contains=article_title_keyword)
    sort_param_key = {
        SortBy.Time: 'likes',  # we don't have TIME information yet
        SortBy.Likes: 'likes',
        SortBy.Views: 'views',
    }[sortby]
    sort_param_order = {
        SortOrder.Ascending: '',
        SortOrder.Descending: '-',
    }[order]
    sort_param = sort_param_order + sort_param_key
    articles = articles.order_by(sort_param)
    return articles_count, articles[start_from:(start_from + count)]


def add_article(dic):
    acc_wx_name = dic['wx_name']
    try:
        acc = OfficialAccount.get(wx_id__exact=acc_wx_name)
    except ObjectDoesNotExist:
        acc_name = dic['name']
        acc = OfficialAccount.create(
            wx_id=acc_wx_name,
            name=acc_name,
            description=acc_name
        )
    art = Article.model()
    art.official_account_id = acc.id
    for attr in ['title', 'description', 'avatar_url', 'url', 'likes', 'views']:
        setattr(art, attr, dic[attr])
    try:
        art.save()
        return True
    except IntegrityError:
        return False


def get_articles_by_official_account_id(id):
    return Article.filter(official_account_id__exact=id)


# Messages

def get_messages(category=None, official_account_id=None, only_unprocessed=None):
    messages = Message.all()
    if official_account_id:
        messages = messages.filter(official_account__id__exact=official_account_id)
    if category and category != MessageCategory.All:
        messages = messages.filter(category__exact=category)
    if only_unprocessed:
        messages = messages.filter(processed__exact=True)
    return messages


def process_message(message_id):
    try:
        message = Message.get(pk=message_id)
        message.processed = True
        message.save()
        return True
    except ObjectDoesNotExist:
        return False


def add_message(category, official_account_id, title, content, admin_name=None):
    try:
        message = Message.model()
        message.category = category
        if int(category) == MessageCategory.ToStudent:
            admin = Admin.get(pk=admin_name)
            message.admin = admin
        message.official_account = OfficialAccount.get(pk=official_account_id)
        message.title = title
        message.content = content
        message.processed = False
        message.save()
        return True
    except ObjectDoesNotExist:
        return False
