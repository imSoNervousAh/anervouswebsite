# -*- coding: utf-8 -*-

import backend
import daemon
import setup_db

from django.db import connection

from subprocess import call
import datetime

setup_db.setup()


def get_date_object_before_n_days(n):
    return datetime.date.today() - datetime.timedelta(days=n)


def clean_test_db():
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


def build_test_db():
    clean_test_db()

    admin_w = Admin.create(username='w', password='x', description='www')
    admin_wyl = Admin.create(username='wyl8899', password='xxxxxxxx', description='韦毅龙')
    admin_ytl = Admin.create(username='ytl14', password='shenmegui', description='杨基龙')
    for id_suffix in ['417', '310', '434', '416']:
        id = '2014011%s' % id_suffix
        backend.add_admin(id, '0', id_suffix)

    oa_mu = OfficialAccount.create(name='Lab Mu', wx_id='mulab_thu')
    Application.create(official_account=oa_mu, user_submit='FANG KUAI', status='not_submitted')
    oa_mz = OfficialAccount.create(name='谜之公众号', description='有换行的哦\n啊\n', wx_id='mizhigongzhonghao')
    Application.create(official_account=oa_mz, user_submit='2014011417', status='rejected')
    oa_zx = OfficialAccount.create(name='酒井资讯', wx_id='jiujingzixun')
    Application.create(official_account=oa_zx, user_submit='2014011416', status='pending')
    oa_yandujian = OfficialAccount.create(name='清华研读间', wx_id='qinghuayandujian')
    Application.create(official_account=oa_yandujian, user_submit='2014011434', status='pending')

    message_test_db(oa_zx.id)

    update()
