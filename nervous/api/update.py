from database import backend
from api import getdata
import time
import datetime


def get_time_string_before_n_days(n):
    seconds_of_day = 60 * 60 * 24;
    target_time = time.localtime(time.time() - n * seconds_of_day)
    return time.strftime('%Y-%m-%d', target_time)


def get_date_object_before_n_days(n):
    return datetime.date.today() - datetime.timedelta(days=n)


def get_time_string_before_month():
    return get_time_string_before_n_days(30)


def get_time_string_now():
    return get_time_string_before_n_days(0)


def add_items(dic):
    for temp in dic:
        temp['official_account_name'] = temp['name']
        temp['description'] = temp['content']
        temp['views'] = temp['readnum']
        temp['likes'] = temp['likenum']
        temp['avatar_url'] = temp['picurl']
        temp['update_time'] = get_time_string_now()
        backend.add_article(temp)


def update_official_account(account):
    print 'updating official account: %s' % account

    paras = {
        'wx_name': account,
        'datestart': get_time_string_before_month(),
        'dateend': get_time_string_now()
    }

    d = getdata.get_dict('wx/opensearchapi/content_list', paras)
    totnum = d['returnData']['total']
    ind = (d['returnData'])['items']
    add_items(ind)
    totnum -= 10
    cnt = 10
    while totnum > 0:
        paras['start'] = cnt
        d = getdata.get_dict('wx/opensearchapi/content_list', paras)
        d1 = (d['returnData'])['items']
        add_items(d1)
        totnum -= 10
        cnt += 10


def update_official_account_nums_before_n_days(account, n):
    day_string = get_time_string_before_n_days(n)

    paras = {
        'wx_name': account,
        'beginDate': day_string,
        'endDate': day_string
    }
    d = getdata.get_dict('wx/opensearchapi/nickname_order_total', paras)

    res = d['returnData']
    dic = {
        'date': get_date_object_before_n_days(n),
        'likes': res.get('likenum_total', 0),
        'views': res.get('readnum_total', 0),
        'articles': res.get('url_num_total', 0)
    }
    backend.add_account_record(account, dic)


def update_official_account_nums(account):
    for i in xrange(1, 9):
        update_official_account_nums_before_n_days(account, i)


def update_all():
    lists = backend.get_official_accounts_wx_name()
    for account in lists:
        update_official_account(account)
        update_official_account_nums(account)
