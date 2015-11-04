from database import backend
from api import getdata
import time

delta = 60 * 60 * 24 * 30


def add_items(dic):
    for temp in dic:
        temp['official_account_name'] = temp['name']
        temp['description'] = temp['content']
        temp['views'] = temp['readnum']
        temp['likes'] = temp['likenum']
        temp['avatar_url'] = temp['picurl']
        temp['update_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        backend.add_article(temp)


def update_official_account(account):
    print 'updating.......'
    paras = {}
    paras['wx_name'] = account
    paras['datestart'] = time.strftime('%Y-%m-%d', time.localtime(time.time() - delta))
    paras['dateend'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # paras['start'] = 0
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


def update_all():
    # TODO: backend should return a list of wx_id
    # lists = backend.get_official_accounts_wx_name()
    lists = ['jiujingzixun']
    for i in lists:
        update_official_account(i)
