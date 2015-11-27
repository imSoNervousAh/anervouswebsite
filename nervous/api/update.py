import database.gsdata_utils
from api import getdata
import time
import datetime
import socket
import re
import requests


def get_time_string_before_n_days(n):
    seconds_of_day = 60 * 60 * 24
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
        database.gsdata_utils.add_article(temp)


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
        'articles': res.get('url_num_total', 0),
    }
    # Maybe gsdata hasn't got the data ...
    if dic['views'] > 0:
        database.gsdata_utils.add_account_record(account, dic)


def update_official_account_daily_nums(account):
    for i in xrange(1, 9):
        update_official_account_nums_before_n_days(account, i)


def get_wci(account):
    try:
        paras = {'wx_name': account}
        d = getdata.get_dict('wx/opensearchapi/nickname_order_now', paras)
        return d['returnData']['items'][0]['wci']
    except IndexError:
        print 'WCI fetching for %s fails, trying brute force...' % account
        url = 'http://www.gsdata.cn/query/wx?q=%s&search_field=2' % account
        text = requests.get(url, timeout=7).text
        g = re.search(r"class=\"hm\">\r\n(.*?)<", text)
        return float(g.group(1))


def update_official_account_nums(account):
    paras = {'wx_name': account}
    d = getdata.get_dict('wx/opensearchapi/nickname_order_total', paras)
    res = d['returnData']
    res_dic = {
        'likes_total': res['likenum_total'],
        'views_total': res['readnum_total'],
        'wci': get_wci(account),
    }
    database.gsdata_utils.update_account_nums(account, res_dic)


def update_all(account):
    try:
        update_official_account(account)
        update_official_account_nums(account)
        update_official_account_daily_nums(account)
    except (KeyError, IndexError):
        print u'update of account %s failed due to gsdata error' % account
    except socket.timeout:
        print u'update of account %s failed due to network error' % account


def verify_wx_name(wx_name):
    try:
        params = {'wx_name': wx_name}
        d = getdata.get_dict('wx/wxapi/nickname_one', params)
        return d['returnCode'] == '1001'
    except:
        return None
