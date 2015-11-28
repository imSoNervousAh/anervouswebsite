# coding=utf-8

from models import *
import api.update as api_update
import api.backend_utils
from api import sendemail
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import datetime
import time
from multiprocessing import Process
import traceback


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
    return Application.objects.get(pk=id)


def application_from_dict(dic, base=None):
    application = base or Application.objects.model()
    for attr in [
        'manager_name', 'manager_student_id',
        'manager_dept', 'manager_tel', 'manager_email',
        'user_submit', 'association', 'status', 'reject_reason']:
        # NOTE: invocation that lacks parameter can not happen with real POST
        # so if you see '__placeholder__' in database, THAT INDICATES A BUG
        val = dic.get(attr, '__placeholder__')
        setattr(application, attr, val)
    application.clean_fields(exclude=['official_account'])
    return application


def official_account_from_dict(dic):
    account = OfficialAccount.objects.model()
    for attr in ['name', 'description', 'wx_id']:
        setattr(account, attr, dic.get(attr, '__placeholder__'))
    account.full_clean(validate_unique=False)
    if not settings.ALLOW_INVALID_WX_NAME:
        res = api.backend_utils.verify_wx_name(account.wx_id)
        if res == None:
            raise ValidationError({
                'wx_id': u'无法验证ID合法性，请稍后再试',
            })
        if res == False:
            raise ValidationError({
                'wx_id': u'请输入一个合法的公众号ID',
            })
    return account


def add_application(dic):
    application = application_from_dict(dic)
    account = official_account_from_dict(dic)
    account.full_clean()
    account.save()
    application.official_account = account
    application.full_clean()
    application.save()


def student_modify_application(dic):
    application_id = int(dic['id'])
    application = get_application_by_id(application_id)
    status = application.status
    assert (status == 'not_submitted' or status == 'rejected')
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
    id = app['id']
    application = Application.objects.get(pk=id)
    assert (application.status == 'pending')
    for attr in ['status', 'operator_admin']:
        setattr(application, attr, app.get(attr, '__unknown__'))
    if app['status'] == 'rejected':
        application.reject_reason = app['reject_reason']
    application.full_clean()
    application.save()
    if application.status == 'approved' and settings.UPDATE_UPON_APPROVING:
        def worker():
            try:
                api_update.update_all(application.official_account.wx_id)
            except Exception as e:
                traceback.print_exc()

        p = Process(target=worker)
        p.start()


def del_application(id):
    application = Application.objects.get(pk=id)
    assert (application.status == 'not_submitted')
    application.official_account.delete()


def recall_application(id):
    account = OfficialAccount.objects.get(pk=id)
    application = account.application
    assert (application.status == 'pending')
    application.status = 'not_submitted'
    application.save()


# Official Accounts

def get_official_accounts():
    return OfficialAccount.objects.all().filter(application__status__exact='approved')


def get_official_account_by_id(id):
    return OfficialAccount.objects.get(pk=id)


def get_official_accounts_with_unprocessed_messages(category):
    return OfficialAccount.objects \
        .filter(
        message__processed__exact=False,
        message__category__exact=category
    ).distinct()


def del_official_account(id):
    account = OfficialAccount.objects.get(pk=id)
    account.delete()
    get_articles_by_official_account_id(id).delete()


# Admins

def add_admin(username, md5_password, email, description):
    admin = Admin.objects.model()
    admin.username = username
    admin.password = md5_password
    admin.email = email
    admin.description = description
    admin.full_clean()
    admin.save()


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


def process_all_messages(official_account_id, category):
    messages = get_messages(
        official_account_id=official_account_id,
        only_unprocessed=True,
        category=category
    )
    for message in messages:
        message.processed = True
        message.save()
    return True


def add_message(category, official_account_id, content, admin_name=None):
    message = Message.objects.model()
    category = int(category)
    message.category = category
    if int(category) == MessageCategory.ToStudent:
        admin = Admin.objects.get(pk=admin_name)
        message.admin = admin
    else:
        message.admin = None
    message.official_account = OfficialAccount.objects.get(pk=official_account_id)
    message.content = content
    message.processed = False
    message.full_clean(exclude=['admin'])
    opposite_category = MessageCategory.ToAdmin + MessageCategory.ToStudent - category
    process_all_messages(official_account_id, opposite_category)
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


# Forewarn rules

def forewarn_rule_from_dict(dic, base=None):
    rule = base or ForewarnRule.objects.model()
    account_name = dic['account_name']
    if account_name != '':
        try:
            account = OfficialAccount.objects.get(name__exact=account_name)
        except ObjectDoesNotExist:
            raise ValidationError({
                'account_name': u'数据库中没有此公众号',
            })
    else:
        account = None
    rule.account = account
    for attr in ['duration', 'notification', 'target', 'value']:
        setattr(rule, attr, dic[attr])
    rule.full_clean()
    return rule


def add_forewarn_rule(dic):
    rule = forewarn_rule_from_dict(dic)
    rule.save()


def modify_forewarn_rule(dic):
    rule = ForewarnRule.objects.get(pk=dic['id'])
    forewarn_rule_from_dict(dic, rule).save()


def get_forewarn_rules():
    return ForewarnRule.objects.all()


def get_forewarn_rule_by_id(id):
    return ForewarnRule.objects.get(pk=id)


def del_forewarn_rule(id):
    get_forewarn_rule_by_id(id).delete()


def get_forewarn_records():
    return ForewarnRecord.objects.all()


def delete_expired_rules():
    records = get_forewarn_rules()
    for record in records:
        delta = datetime.timedelta(days=record.duration)
        expire_time = record.time + delta
        if expire_time < timezone.now():
            record.delete()


# Forewarning

def get_lastest_record_date(account):
    try:
        return get_latest_record(account.id).date
    except IndexError:
        return datetime.date.fromtimestamp(0)


def email_to_admins(id):
    admins = get_admins()
    for admin in admins:
        sendemail.email_rule_id(admin.email, admin.description, id)


def report_forewarn_record(record):
    subject = u'report_forewarn_record'
    content = record.__unicode__()
    print '%s: %s' % (subject, content)
    email_to_admins(record.id)


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


def check_forewarn_rule(rule, pending_check_accounts):
    account = rule.account
    if account:
        if account.update_status == OfficialAccount.PENDING_CHECK_STATUS:
            check_forewarn_rule_on_account(rule, account)
    else:
        for account in pending_check_accounts:
            check_forewarn_rule_on_account(rule, account)


def check_all_forewarn_rules():
    rules = get_forewarn_rules()
    pending_check_accounts = OfficialAccount.objects.filter(
        update_status__exact=OfficialAccount.PENDING_CHECK_STATUS
    )
    print pending_check_accounts
    for rule in rules:
        check_forewarn_rule(rule, pending_check_accounts)


def save_account_update_status(account, status):
    account.update_status = status
    account.save(update_fields=['update_status'])


def release():
    accounts = OfficialAccount.objects.all()
    for account in accounts:
        save_account_update_status(account, OfficialAccount.NORMAL_STATUS)


def update_progress():
    updated = OfficialAccount.objects.filter(
        Q(update_status=OfficialAccount.UPDATED_STATUS) |
        Q(update_status=OfficialAccount.PENDING_CHECK_STATUS) |
        Q(update_status=OfficialAccount.FINISHED_STATUS)
    ).count()
    total = OfficialAccount.objects.exclude(
        update_status=OfficialAccount.NORMAL_STATUS
    ).count()
    if total == 0:
        return 100
    else:
        return updated * 100 / total


def updating_account_name():
    try:
        account = OfficialAccount.objects.get(
            update_status=OfficialAccount.UPDATING_STATUS
        )
        return account.name
    except ObjectDoesNotExist:
        return ''


def update_all():
    accounts = get_official_accounts()

    for account in accounts:
        # Another update already in progress, abort
        if account.update_status != OfficialAccount.NORMAL_STATUS:
            print "Aborted"
            return

    try:
        # Acquire the "lock"
        for account in accounts:
            account.update_status = OfficialAccount.PENDING_UPDATE_STATUS
            # NOTE: this attribute will not be saved into the database
            account.lastest_record_date = get_lastest_record_date(account)
            print "lastest: ", account, account.lastest_record_date
            save_account_update_status(account, OfficialAccount.PENDING_UPDATE_STATUS)

        for account in accounts:
            save_account_update_status(account, OfficialAccount.UPDATING_STATUS)
            # Wait for front-end
            time.sleep(2)
            api_update.update_all(account.wx_id)
            save_account_update_status(account, OfficialAccount.UPDATED_STATUS)
            print update_progress()

        for account in accounts:
            new_lastest_record_date = get_lastest_record_date(account)
            print "new_lastest: ", account, new_lastest_record_date
            if account.lastest_record_date != new_lastest_record_date:
                status = OfficialAccount.PENDING_CHECK_STATUS
            else:
                status = OfficialAccount.FINISHED_STATUS
            save_account_update_status(account, status)

        check_all_forewarn_rules()
    finally:
        # Wait for front-end
        time.sleep(2)

        # Release the "lock"
        release()

        delete_expired_rules()


# Global

def get_globals():
    try:
        return Globals.objects.get()
    except ObjectDoesNotExist:
        return Globals.objects.create()


def modify_announcement(announcement):
    g = get_globals()
    g.announcement = announcement
    g.full_clean()
    g.save()


def get_announcement():
    g = get_globals()
    return g.announcement
