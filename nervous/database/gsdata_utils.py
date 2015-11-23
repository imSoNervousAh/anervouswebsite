from models import *

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings

import pytz
import datetime


def get_official_accounts():
    return OfficialAccount.objects.all().filter(application__status__exact='approved')


def get_official_accounts_wx_name():
    return map(lambda account: account.wx_id, get_official_accounts())


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
    naive_time = datetime.datetime.strptime(dic['posttime'], "%Y-%m-%d %H:%M:%S")
    art.posttime = pytz.timezone(settings.TIME_ZONE).localize(naive_time, is_dst=None)
    for attr in ['title', 'description', 'avatar_url', 'url', 'likes', 'views']:
        setattr(art, attr, dic[attr])
    try:
        art.save()
        return True
    except IntegrityError:
        return False


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
