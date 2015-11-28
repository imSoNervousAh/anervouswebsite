import datetime
import re
import requests
import socket
import time
import math
import database.gsdata_utils
import database.models
from api import getdata


def calculate_wci(r, r_max, z, z_max, n):
    r_index = 0.4 * math.log(r + 1) + \
              0.45 * math.log(float(r) / n + 1) + \
              0.15 * math.log(r_max + 1)
    z_index = 0.4 * math.log(10 * z + 1) + \
              0.45 * math.log(10 * float(z) / n + 1) + \
              0.15 * math.log(10 * z_max + 1)
    total_index = 0.8 * r_index + 0.2 * z_index
    wci = total_index ** 2 * 10
    print 'calculate_wci:', r, r_max, z, z_max, n, '=>', wci
    return wci


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


def get_wci(account):
    try:
        paras = {'wx_name': account}
        d = getdata.get_dict('wx/opensearchapi/nickname_order_now', paras)
        return float(d['returnData']['items'][0]['wci'])
    except IndexError:
        print 'WCI fetching for %s fails, trying brute force...' % account
        url = 'http://www.gsdata.cn/query/wx?q=%s&search_field=2' % account
        text = requests.get(url, timeout=7).text
        g = re.search(r"class=\"hm\">\r\n(.*?)<", text)
        return float(g.group(1))


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
    if dic['views'] == 0:
        return False

    database.gsdata_utils.add_account_record(account, dic)
    return True


def update_official_account_daily_nums(account):
    account_instance = database.models.OfficialAccount.objects \
        .get(wx_id=account)
    for i in xrange(1, 9):
        date = get_date_object_before_n_days(i)
        ret = update_official_account_nums_before_n_days(account, i)
        if not ret:
            continue
        record = database.models.AccountRecord.objects \
            .get(account=account_instance, date=date)

        def tz_time_before_n_days(i):
            date = get_date_object_before_n_days(i)
            return database.gsdata_utils.tz_time_from_naive_time(
                datetime.datetime(date.year, date.month, date.day)
            )

        end_time = tz_time_before_n_days(i - 1)
        start_time = tz_time_before_n_days(i)
        articles = database.models.Article.objects \
            .filter(official_account_id=account_instance.id) \
            .filter(posttime__lte=end_time) \
            .filter(posttime__gte=start_time)
        max_r, max_z, r, z = 0, 0, 0, 0
        for article in articles:
            max_r = max(max_r, article.views)
            max_z = max(max_z, article.likes)
            r = r + article.views
            z = z + article.likes
        record.wci = calculate_wci(r, max_r, z, max_z, articles.count())
        record.save()


def update_official_account_nums(account):
    paras = {'wx_name': account}
    d = getdata.get_dict('wx/opensearchapi/nickname_order_total', paras)
    res = d['returnData']
    res_dic = {
        'likes_total': res['likenum_total'],
        'views_total': res['readnum_total'],
        'wci': get_wci(account)
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
