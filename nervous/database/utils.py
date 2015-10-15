# -*- coding: utf-8 -*-
from backend import *
from api import getdata

def test_add_article():
    paras = {}
    paras['wx_name'] = 'jiujingzixun'
    d = getdata.get_dict('wx/opensearchapi/content_list', paras)
    ind = (d['returnData'])['items']
    for temp in ind:
        temp['official_account_name'] = temp['name']
        temp['description'] = temp['content']
        temp['views'] = temp['readnum']
        temp['likes'] = temp['likenum']
        print temp
        add_article(temp)
    

def build_test_db():
    Admin.create(username='wyl8899', password='xxxxxxxx', description='韦毅龙')
    Admin.create(username='ytl14', password='shenmegui', description='杨基龙')

    mu = OfficialAccount.create(name='Lab Mu')
    Application.create(official_account=mu, user_submit='FANG KUAI', status='not_submitted')
    mus = OfficialAccount.create(name='Lab Mu\'s')
    Application.create(official_account=mus, user_submit='GayLou', status='pending')

    test_add_article()


def clean_test_db():
    for model in [Admin, OfficialAccount, Application, Article]:
        model.all().delete()
