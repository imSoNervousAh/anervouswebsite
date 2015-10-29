# -*- coding: utf-8 -*-

from subprocess import call

from api import getdata, update
import backend
import setup_db

setup_db.setup()

def clean_test_db():
    call(["python", "manage.py", "flush", "--noinput"])
    call(["python", "manage.py", "sqlsequencereset", "database"])

# test gsdata

def test_update():
    update.update_all()

# build a db for testing

def build_offline_test_db():
    clean_test_db()

    admin_wyl = Admin.create(username='wyl8899', password='xxxxxxxx', description='韦毅龙')
    admin_ytl = Admin.create(username='ytl14', password='shenmegui', description='杨基龙')

    mu = OfficialAccount.create(name='Lab Mu')
    Application.create(official_account=mu, user_submit='FANG KUAI', status='not_submitted')
    zx = OfficialAccount.create(name='酒井资讯', wx_id='jiujingzixun')
    Application.create(official_account=zx, user_submit='2014011416', status='pending')

    assert(backend.add_message(
        MessageCategory.ToAdmin, zx.id,
        'to_admin_title', 'to_admin_content'
    ))
    assert(backend.add_message(
        MessageCategory.ToStudent, zx.id,
        'to_student_title', 'to_student_content',
        'wyl8899'
    ))
    assert(backend.add_message(
        MessageCategory.ToAdmin, zx.id,
        'yet_another_title', 'yet_another_content'
    ))

    backend.set_student_information(2014011434, 'wyl')


def build_test_db():
    build_offline_test_db()
    test_update()
