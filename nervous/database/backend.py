# coding=utf-8
from models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from api import sendemail
import pytz


# Applications

def get_applications():
    return Application.objects.all()


def get_applications_by_status(status):
    return Application.objects.filter(status__exact=status)


def get_pending_applications():
    return get_applications_by_status('pending')


def get_applications_by_user(username):
    return Application.objects.filter(user_submit__exact=username)


def get_applications_by_admin(username):
    return Application.objects.filter(operator_admin__exact=username)


def get_application_by_id(id):
    return Application.objects.get(official_account__id__exact=id)


def application_from_dict(dic, base=None):
    application = base or Application.objects.model()
    for attr in [
            'manager_name', 'manager_student_id',
            'manager_dept', 'manager_tel', 'manager_email',
            'user_submit', 'association', 'status']:
        # NOTE: invocation that lacks parameter can not happen with real POST
        # so if you see '__placeholder__' in database, THAT INDICATES A BUG
        val = dic.get(attr, '__placeholder__')
        setattr(application, attr, val)
    application.clean_fields(exclude=['official_account'])
    return application


def official_account_from_dict(dic):
    oa = OfficialAccount.objects.model()
    for attr in ['name', 'description', 'wx_id']:
        setattr(oa, attr, dic[attr])
    oa.full_clean(validate_unique=False)
    return oa


def add_application(dic):
    application = application_from_dict(dic)
    account = official_account_from_dict(dic)
    account.full_clean()
    account.save()
    application.official_account = account
    application.full_clean()
    application.save()


def student_modify_application(dic):
    print dic
    application_id = int(dic['application_id'])
    application = get_application_by_id(application_id)
    old_account = application.official_account
    account = official_account_from_dict(dic)
    application = application_from_dict(dic, base=application)
    if old_account.wx_id != account.wx_id:
        account.full_clean()
    old_account.delete()
    account.full_clean()
    account.save()
    application.official_account = account
    application.full_clean()
    application.save()


def modify_application(app):
    print app
    try:
        account = OfficialAccount.objects.get(pk=app['account_id'])
        application = Application.objects.get(pk=account)
        for attr in ['status', 'operator_admin']:
            setattr(application, attr, app.get(attr, "unknown"))
        application.save()
    except ObjectDoesNotExist:
        return False


def del_application(id):
    try:
        oa = OfficialAccount.objects.get(pk=id)
        oa.delete()
        return True
    except ObjectDoesNotExist:
        return False


# Official Accounts

def get_official_accounts():
    return OfficialAccount.objects.all().filter(application__status__exact='approved')


def get_official_accounts_wx_name():
    return map(lambda account: account.wx_id, get_official_accounts())


def get_official_account_by_id(id):
    return OfficialAccount.objects.get(pk=id)


def get_official_accounts_with_unprocessed_messages():
    return OfficialAccount.objects.filter(message__processed__exact=False).distinct()


def del_official_account(id):
    try:
        account = OfficialAccount.objects.get(pk=id)
        account.delete()
        return True
    except ObjectDoesNotExist:
        return False


# Account Record

def add_account_record(wx_id, dic):
    account = OfficialAccount.objects.get(wx_id__exact=wx_id)
    date = dic['date']
    try:
        old_record = account.accountrecord_set.get(date__exact=date)
        old_record.delete()
    except ObjectDoesNotExist:
        pass
    record = AccountRecord.objects.model()
    record.account = account
    record.date = date
    for attr in ['likes', 'views', 'articles']:
        setattr(record, attr, dic.get(attr, -1))
    record.save()


# Admins

def add_admin(username, md5_password, email, description):
    try:
        Admin.objects.create(
            username=username,
            password=md5_password,
            email=email,
            description=description
        )
        return True
    except IntegrityError:
        return False


def del_admin(username):
    try:
        admin = Admin.objects.get(username=username)
        admin.delete()
        return True
    except ObjectDoesNotExist:
        return False


def get_admins():
    return Admin.objects.all()


def get_admin_emails():
    return map(lambda x: x.email, get_admins())


def check_admin(username, password):
    try:
        admin = Admin.objects.get(username=username)
        return admin.password == password
    except ObjectDoesNotExist:
        return False


# Students

def get_student_by_id(student_id):
    return Student.objects.get(pk=student_id)


def set_student_information(student_id, dic):
    try:
        student = Student.objects.create(student_id=student_id)
    except IntegrityError:
        student = Student.objects.get(pk=student_id)
    for attr in ['real_name', 'dept', 'tel', 'email']:
        # Again, __placeholder__ exists for the sake of database.tests
        setattr(student, attr, dic.get(attr, '__placeholder__'))
    student.full_clean()
    student.save()


def check_student_information_filled(student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except ObjectDoesNotExist:
        student = Student.objects.create(student_id=student_id)
    return student.information_filled()


# Articles

def get_articles(sortby=SortBy.Time, order=SortOrder.Descending, start_from=0, count=10, filter=None):
    articles = Article.objects.all()
    filter = filter or {}
    official_account_id = filter.get('official_account_id', None)
    article_title_keyword = filter.get('article_title_keyword', None)
    posttime_begin = filter.get('posttime_begin', None)
    posttime_end = filter.get('posttime_end', None)
    if official_account_id:
        articles = articles.filter(official_account_id__exact=official_account_id)
    if article_title_keyword:
        articles = articles.filter(title__contains=article_title_keyword)
    if posttime_begin:
        articles = articles.filter(posttime__gte=posttime_begin)
    if posttime_end:
        articles = articles.filter(posttime__lte=posttime_end)
    articles_count = articles.count()

    sort_param_key = {
        SortBy.Time: 'posttime',
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
        acc = OfficialAccount.objects.get(wx_id__exact=acc_wx_name)
    except ObjectDoesNotExist:
        acc_name = dic['name']
        acc = OfficialAccount.objects.create(
            wx_id=acc_wx_name,
            name=acc_name,
            description=acc_name
        )
    art = Article.objects.model()
    art.official_account_id = acc.id
    naive_time = datetime.strptime(dic['posttime'], "%Y-%m-%d %H:%M:%S")
    art.posttime = pytz.timezone(settings.TIME_ZONE).localize(naive_time, is_dst=None)
    for attr in ['title', 'description', 'avatar_url', 'url', 'likes', 'views']:
        setattr(art, attr, dic[attr])
    try:
        art.save()
        return True
    except IntegrityError:
        return False


def get_articles_by_official_account_id(id):
    return Article.objects.filter(official_account_id__exact=id)


# Messages

def get_messages(category=None, official_account_id=None, only_unprocessed=None):
    messages = Message.objects.all()
    if official_account_id:
        messages = messages.filter(official_account__id__exact=official_account_id)
    if category and category != MessageCategory.All:
        messages = messages.filter(category__exact=category)
    if only_unprocessed:
        messages = messages.filter(processed__exact=False)
    return messages


def process_all_messages(official_account_id):
    messages = get_messages(
        official_account_id=official_account_id,
        only_unprocessed=True
    )
    for message in messages:
        message.processed = True
        message.save()
    return True


def add_message(category, official_account_id, content, admin_name=None):
    message = Message.objects.model()
    message.category = category
    if int(category) == MessageCategory.ToStudent:
        process_all_messages(official_account_id)
        admin = Admin.objects.get(pk=admin_name)
        message.admin = admin
    else:
        message.admin = None
    message.official_account = OfficialAccount.objects.get(pk=official_account_id)
    message.content = content
    message.processed = False
    message.full_clean(exclude=['admin'])
    message.save()

# Account records

def get_records(official_account_id, day_start, day_end):
    return AccountRecord.objects \
        .filter(account__id__exact=official_account_id) \
        .filter(date__gte=day_start) \
        .filter(date__lte=day_end)


def get_views(account, day_start, day_end):
    records = get_records(account, day_start, day_end)
    return map(lambda rec: rec.views, records)


def get_latest_record(official_account_id):
    return AccountRecord.objects \
        .filter(account__id__exact=official_account_id) \
        .order_by('-date')[0]


# Forewarning

def add_forewarn_rule(dic):
    print dic
    try:
        rule = ForewarnRule.objects.model()
        account_name = dic['account_name']
        if account_name != '':
            account = OfficialAccount.objects.get(name__exact=account_name)
        else:
            account = None
        rule.account = account
        for attr in ['duration', 'notification', 'target', 'value']:
            setattr(rule, attr, int(dic[attr]))
        rule.full_clean(exclude=['account'])
        rule.save()
        return True
    except (ObjectDoesNotExist, ValueError):
        return False


def get_forewarn_rules():
    return ForewarnRule.objects.all()


def get_forewarn_records():
    return ForewarnRecord.objects.all()


def email_to_admins(subject, content):
    sendemail.send_mail(get_admin_emails(), subject, content)


def report_forewarn_record(record):
    subject = u'report_forewarn_record'
    content = record.__unicode__()
    print '%s: %s' % (subject, content)
    # email_to_admins(get_admin_emails(), subject, content)


def forewarn_record_from_rule(rule, account):
    return ForewarnRecord.objects.create(
        target=rule.target,
        value=rule.value,
        account=account
    )


def report_if(cond, rule, account):
    if cond:
        record = forewarn_record_from_rule(rule, account)
        report_forewarn_record(record)


def check_forewarn_rule_on_account(rule, account):
    # print "check_forewarn_rule_on_account: %s on %s" % (rule, account)
    try:
        if rule.target == ForewarnTarget.ViewsTotal:
            rec = get_latest_record(account.id)
            report_if(rec.views > rule.value, rule, account)
    except IndexError:
        pass


def check_forewarn_rule(rule):
    if rule.account:
        accounts = [rule.account]
    else:
        accounts = get_official_accounts()
    for account in accounts:
        check_forewarn_rule_on_account(rule, account)


def check_all_forewarn_rules():
    rules = get_forewarn_rules()
    for rule in rules:
        check_forewarn_rule(rule)
