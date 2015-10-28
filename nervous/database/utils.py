# -*- coding: utf-8 -*-

from subprocess import call

from api import getdata, update
import backend
import setup_db

setup_db.setup()

def clean_test_db():
    call(["python", "manage.py", "flush", "--noinput"])
    call(["python", "manage.py", "sqlsequencereset", "database"])

# test add database models

def test_add_admins():
    Admin.create(username='wyl8899', password='xxxxxxxx', description='韦毅龙')
    Admin.create(username='ytl14', password='shenmegui', description='杨基龙')

def test_add_students():
    backend.set_student_information(2014011434, 'wyl')

# test gsdata

def test_update():
    update.update_all()

# build a db for testing

def build_test_db():
    clean_test_db()

    mu = OfficialAccount.create(name='Lab Mu')
    Application.create(official_account=mu, user_submit='FANG KUAI', status='not_submitted')
    mus = OfficialAccount.create(name='Lab Mu\'s')
    Application.create(official_account=mus, user_submit='GayLou', status='pending')

    assert(backend.add_message(
        MessageCategory.ToAdmin, mu.id,
        'to_admin_title', 'to_admin_content'
    ))
    assert(backend.add_message(
        MessageCategory.ToStudent, mu.id,
        'to_student_title', 'to_student_content'
    ))
    assert(backend.add_message(
        MessageCategory.ToAdmin, mus.id,
        'yet_another_title', 'yet_another_content'
    ))

    test_add_admins()
    test_add_students()
    test_update()
