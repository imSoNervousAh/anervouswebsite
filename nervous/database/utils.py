# -*- coding: utf-8 -*-
from backend import *


def build_test_db():
    Admin.create(username='wyl8899', password='xxxxxxxx', description='韦毅龙')
    Admin.create(username='ytl14', password='shenmegui', description='杨基龙')
    
    paras = {}
    paras['wx_name'] = 'jiujingzixun'
    d = getdata.get_dict('wx/opensearchapi/content_list', paras)
    ind = (d['returnData'])['items']
    for temp in ind:
        temp['official_account_name'] = temp['name']
        temp['description'] = temp['content']
        temp['views'] = temp['readnum']
        temp['likes'] = temp['likes']
        backend.add_article(temp)
    

    account = OfficialAccount.create(name='Lab Mu')
    Application.create(official_account=account, user_submit='FANG KUAI', status='not_submitted')
    account = OfficialAccount.create(name='Lab Mu\'s')
    Application.create(official_account=account, user_submit='GayLou', status='pending')


def clean_test_db():
    for model in [Admin, OfficialAccount, Application, Article]:
        model.all().delete()
