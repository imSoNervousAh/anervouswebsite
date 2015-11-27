# -*- coding: utf-8 -*-

import datetime
import hashlib
import random
import time
from subprocess import call

from django.conf import settings
from django.db import connection

import backend
import gsdata_utils
from models import *
import api.bind_domain

# Utils

def get_date_object_before_n_days(n):
    return datetime.date.today() - datetime.timedelta(days=n)


def django_admin(cmd):
    call(['python', 'manage.py', cmd])


def migrate():
    django_admin('migrate')


def make_migrations():
    django_admin('makemigrations')


def md5_hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


# Test DB

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
    migrate()


# test gsdata

def update():
    backend.update_all()


# build a db for testing

def message_test_db(message_test_oa_id):
    backend.add_message(
        MessageCategory.ToAdmin, message_test_oa_id,
        'to_admin_content'
    )
    backend.add_message(
        MessageCategory.ToStudent, message_test_oa_id,
        'to_student_content',
        'wyl8899'
    )
    backend.add_message(
        MessageCategory.ToAdmin, message_test_oa_id,
        'yet_another_content'
    )


def forewarn_test_db(name):
    backend.add_forewarn_rule({
        'account_name': name,
        'duration': str(1),
        'notification': str(0),
        'target': str(0),
        'value': str(10000),
    })
    backend.add_forewarn_rule({
        'account_name': name,
        'duration': str(1),
        'notification': str(0),
        'target': str(0),
        'value': str(5),
    })
    backend.add_forewarn_rule({
        'account_name': '',
        'duration': str(1),
        'notification': str(0),
        'target': str(0),
        'value': str(5),
    })


def build_test_db():
    clean_test_db()

    admin_w = Admin.objects.create(username='w', password=md5_hash('x'), description='www', email='huzecong@163.com')
    admin_wyl = Admin.objects.create(username='wyl8899', password=md5_hash('xxxxxxxx'), description=u'韦毅龙',
                                     email='wyl8899k@gmail.com')
    admin_ytl = Admin.objects.create(username='ytl14', password=md5_hash('shenmegui'), description=u'杨基龙',
                                     email='yangtianlong111@gmail.com')
    if settings.DEBUG:
        for id_suffix in ['417', '310', '434', '416']:
            id = '2014011%s' % id_suffix
            backend.add_admin(id, '0', 'fake_student@nervous.gq', id_suffix)

    backend.add_application({
        'name': 'Lab Mu',
        'wx_id': 'mulab_thu',
        'status': 'not_submitted',
    })
    backend.add_application({
        'name': u'酒井资讯',
        'wx_id': 'jiujingzixun',
        'user_submit': '2014011416',
        'status': 'pending',
        'manager_name': u'黄大大',
        'manager_student_id': '2014011416',
        'manager_dept': u'贵系',
        'manager_tel': '12345678901',
        'association': u'贵系学生会'
    })
    backend.add_application({
        'name': u'清华研读间',
        'wx_id': 'qinghuayandujian',
        'description': 'description',
        'status': 'pending',
        'manager_name': u'黄大大',
        'manager_student_id': '2014011416',
        'manager_dept': u'贵系',
        'manager_tel': '12345678901',
        'association': u'贵校'
    })

    oa = OfficialAccount.objects.get(wx_id='jiujingzixun')
    message_test_db(oa.id)
    forewarn_test_db(oa.name)

    update()


def build_large_test_db():
    clean_test_db()

    admin_w = Admin.objects.create(username='w', password=md5_hash('x'), description='www', email='huzecong@163.com')
    if settings.DEBUG:
        for id_suffix in ['417', '310', '434', '416']:
            id = '2014011%s' % id_suffix
            backend.add_admin(id, '0', 'fake_student@nervous.gq', id_suffix)

    n_applications = {
        'pending': 500,
        'approved': 500,
        'rejected': 500,
        'not_submitted': 500,
    }
    for status, count in n_applications.items():
        for i in range(0, count):
            app = {
                'name': u'第' + str(i + 1) + u'个' + status + u'公众号',
                'description': u'第' + str(i + 1) + u'个' + status + u'公众号',
                'wx_id': status + str(i + 1),
                'user_submit': '2014011417',
                'status': status,
                'manager_name': u'黄大大',
                'manager_student_id': '2014011416',
                'manager_dept': u'贵系',
                'manager_tel': '12345678901',
                'association': u'贵校'
            }
            if status == 'rejected':
                app['reject_reason'] = u'任性'
            backend.add_application(app)

        print 'done', status

    n_articles = 10000
    genres = ['abstract', 'animals', 'business', 'cats', 'city', 'food', 'nightlife',
              'fashion', 'people', 'nature', 'sports', 'technics', 'transport']
    n_genres = len(genres)
    for i in range(0, n_articles):
        article = {
            'official_account_name': u'第1个approved公众号',
            'wx_name': 'approved1',
            'title': u'第' + str(i + 1) + u'篇文章',
            'description': u'第' + str(i + 1) + u'篇文章',
            'views': random.randint(0, int(1e8)),
            'likes': random.randint(0, int(1e8)),
        }
        width = random.randint(100, 1000)
        height = random.randint(100, 1000)
        genre = genres[random.randint(0, n_genres - 1)]
        article['name'] = article['official_account_name']
        article['avatar_url'] = ('http://lorempixel.com/%d/%d/%s/' % (width, height, genre)) + 'A R T I C L E ' + str(i + 1)
        article['url'] = article['avatar_url']
        article['posttime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        article['update_time'] = article['posttime']
        gsdata_utils.add_article(article)

        if i % 1000 == 999:
            print 'done article', i + 1

def bind_domain():
    api.bind_domain.bind()
