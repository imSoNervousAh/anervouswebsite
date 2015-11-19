# -*- coding: utf-8 -*-

import backend
import daemon
from models import *
from django.db import connection
from subprocess import call
import datetime


def get_date_object_before_n_days(n):
    return datetime.date.today() - datetime.timedelta(days=n)


def clean_test_db():
    call(["python", "manage.py", "migrate"])
    call(["python", "manage.py", "flush", "--noinput"])
    call(["python", "manage.py", "sqlsequencereset", "database"])
    cursor = connection.cursor()
    cursor.execute("delete from sqlite_sequence")
    for table in ['official_account', 'message', 'article']:
        command = "delete from sqlite_sequence where name='%s'" % table;
        print command
        cursor.execute(command)
    connection.commit()


# test gsdata

def update():
    daemon.update_all()


# build a db for testing

def message_test_db(message_test_oa_id):
    assert (backend.add_message(
        MessageCategory.ToAdmin, message_test_oa_id,
        'to_admin_title', 'to_admin_content'
    ))
    assert (backend.add_message(
        MessageCategory.ToStudent, message_test_oa_id,
        'to_student_title', 'to_student_content',
        'wyl8899'
    ))
    assert (backend.add_message(
        MessageCategory.ToAdmin, message_test_oa_id,
        'yet_another_title', 'yet_another_content'
    ))


def forewarn_test_db(name):
    assert (backend.add_forewarn_rule({
        'account_name': name,
        'duration': str(1),
        'notification': str(0),
        'target': str(0),
        'value': str(10000),
    }))
    assert (backend.add_forewarn_rule({
        'account_name': name,
        'duration': str(1),
        'notification': str(0),
        'target': str(0),
        'value': str(5),
    }))
    assert (backend.add_forewarn_rule({
        'account_name': '',
        'duration': str(1),
        'notification': str(0),
        'target': str(0),
        'value': str(5),
    }))


def build_test_db():
    clean_test_db()

    admin_w = Admin.objects.create(username='w', password='x', description='www', email='huzecong@163.com')
    admin_wyl = Admin.objects.create(username='wyl8899', password='xxxxxxxx', description=u'韦毅龙', email='wyl8899k@gmail.com')
    admin_ytl = Admin.objects.create(username='ytl14', password='shenmegui', description=u'杨基龙', email='yangtianlong111@gmail.com')
    for id_suffix in ['417', '310', '434', '416']:
        id = '2014011%s' % id_suffix
        backend.add_admin(id, '0', '', id_suffix)

    oa_mu = OfficialAccount.objects.create(name='Lab Mu', wx_id='mulab_thu')
    Application.objects.create(official_account=oa_mu, user_submit='FANG KUAI', status='not_submitted')
    oa_mz = OfficialAccount.objects.create(name=u'谜之公众号', description=u'有换行的哦\n啊\n', wx_id='mizhigongzhonghao')
    Application.objects.create(official_account=oa_mz, user_submit='2014011417', status='rejected')
    oa_zx = OfficialAccount.objects.create(name=u'酒井资讯', wx_id='jiujingzixun')
    Application.objects.create(official_account=oa_zx, user_submit='2014011416', status='pending')
    backend.add_application({'name': u'清华研读间', 'wx_id': 'qinghuayandujian', 'description': 'description'})

    message_test_db(oa_zx.id)
    forewarn_test_db(oa_zx.name)

    update()
