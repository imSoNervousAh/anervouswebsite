# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from  django.shortcuts import render_to_response

import re
import urllib2
import urllib
import cookielib
import codecs
import json

from database import backend
from wechat import session


# index

def index(request):
    # 默认返回学生登录界面
    return render(request, 'login/index.html', {'identity': 'student'})


# login/logout

def login(request, identity='student'):
    print 'login/'
    if identity in ['student', 'administrator', 'superuser']:
        response = render(request, 'login/index.html', {'identity': identity})
        return response
    return to_notfound(request)


def logout(request):
    identity = session.get_identity(request)
    if identity != 'none':
        print 'logout success!'
        session.del_session(request)
        response = login(request, identity)
        return response
    print 'no cookies & logout success!'
    return login(request, 'student')


def check_identity(request, identity):
    print identity, 'identity: ', session.get_identity(request)
    return session.get_identity(request) == identity


# student

def student(request):
    if not check_identity(request, 'student'):
        return login(request, 'student')

    username = session.get_username(request)

    official_account_id = '112'

    return render(request, 'student/index.html', {'username': username,
                                                  'official_account_id': official_account_id,

                                                  })


def student_show_applications(request):
    if not check_identity(request, 'student'):
        return login(request, 'student')

    username = session.get_username(request)

    glyphicons = {'approved': 'glyphicon-ok-sign',
                  'rejected': 'glyphicon-remove-sign',
                  'pending': 'glyphicon-question-sign',
                  'not_submitted': 'glyphicon-info-sign',
                  }
    status_name = {'approved': '已通过审批',
                   'rejected': '审批被拒绝',
                   'pending': '待审批',
                   'not_submitted': '尚未提交',
                   }

    applications = backend.get_applications_by_user(username)
    pending_count = 0
    for app in applications:
        app.status_glyphicon = glyphicons[app.status]
        app.status_name = status_name[app.status]
        if app.status == 'pending':
            pending_count += 1

    return render(request, 'student/show_applications.html', {'applications': applications,
                                                              'pending_count': pending_count,
                                                              })


def student_add_applications(request):
    if not check_identity(request, 'student'):
        return login(request, 'student')

    return render(request, 'student/add_applications.html', {})


# administrator

def admin(request):
    print 'show admin'
    if not check_identity(request, 'administrator'):
        return login(request, 'administrator')

    pending_applications_count = len(backend.get_pending_applications())
    username = session.get_username(request)

    return render(request, 'administrator/index.html', {'username': username,
                                                        'pending_applications_count': pending_applications_count})


def admin_dashboard(request):
    if not check_identity(request, 'administrator'):
        return login(request, 'administrator')

    pending_applications = backend.get_pending_applications()
    official_accounts = backend.get_official_accounts()
    articles_count, articles = backend.get_articles()

    return render(request, 'administrator/dashboard.html', {'pending_applications': pending_applications,
                                                            'official_accounts': official_accounts,
                                                            'articles': articles,
                                                            'articles_count': articles_count,
                                                            })


def admin_show_official_accounts(request):
    if not check_identity(request, 'administrator'):
        return login(request, 'administrator')

    official_accounts = backend.get_official_accounts()

    return render(request, 'administrator/official_accounts.html', {'official_accounts': official_accounts})


def admin_show_articles(request):
    if not check_identity(request, 'administrator'):
        return login(request, 'administrator')

    articles_count, articles = backend.get_articles()

    return render(request, 'administrator/articles.html', {'articles': articles,
                                                           'articles_count': articles_count,
                                                           })


def admin_show_applications(request, type):
    if not check_identity(request, 'administrator'):
        return login(request, 'administrator')

    if type == 'pending':
        applications = backend.get_pending_applications()
        type_name = u'待审批申请'
    elif type == 'processed':
        applications = backend.get_applications_by_status('approved') \
                       | backend.get_applications_by_status('rejected')
        type_name = u'我处理的申请（目前还是所有已审批申请）'
    elif type == 'all':
        applications = backend.get_applications()
        type_name = u'所有申请'
    else:
        applications = []
        type_name = ''

    return render(request, 'administrator/applications.html', {'applications': applications,
                                                               'application_type': type_name,
                                                               })


def admin_show_official_account_detail(request, id):
    if not check_identity(request, 'administrator'):
        return login(request, 'administrator')

    articles_on_one_page = 10
    try:
        page_current = int(request.GET['page'])
    except:
        page_current = 1

    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)
    articles_count, articles = backend.get_articles(start_from=(page_current - 1) * articles_on_one_page,
                                                    count=articles_on_one_page,
                                                    filter={'official_account_id': id})

    page_count = (articles_count + articles_on_one_page - 1) // articles_on_one_page
    pages = xrange(1, page_count + 1)
    '''
    if page_count <= 5:

    elif page_current > 1:

        page['pages'] = xrange(1, 5)
        '''
    page = {'count': page_count,
            'current': page_current,
            'pages': pages}

    return render(request, 'administrator/detail.html', {'account': official_account,
                                                         'articles': articles,
                                                         'articles_count': articles_count,
                                                         'official_account_id': id,
                                                         'page': page,
                                                         })


def admin_message(request, id):
    print 'show admin_message'
    messages = backend.get_messages(official_account_id=id)
    try:
        account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)
    official_accounts = backend.get_official_accounts()

    return render(request, 'administrator/message.html', {'account': account,
                                                          'messages': messages,
                                                          'MessageCategory': MessageCategory,
                                                          'official_account_id': id,
                                                          'official_accounts': official_accounts
                                                          })


# message

def message_detail_admin(request, id, category=MessageCategory.ToStudent):
    messages = backend.get_messages(official_account_id=id)
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    return render(request, 'message/message.html', {'account': official_account,
                                                    'messages': messages,
                                                    'category': category,
                                                    'official_account_id': id,
                                                    'MessageCategory': MessageCategory
                                                    })


def message_detail_student(request, id):
    return message_detail_admin(request, id, MessageCategory.ToAdmin)


# superuser

def superuser(request):
    if not check_identity(request, 'superuser'):
        return login(request, 'superuser')

    return render(request, 'superuser/index.html', {'username': u'超级管理员'})


def superuser_show_admins(request):
    if not check_identity(request, 'superuser'):
        return login(request, 'superuser')

    administrators = backend.get_admins()

    return render(request, 'superuser/admins.html', {'administrators': administrators})


# misc

def notfound(request):
    print '[in] notfound'
    return render(request, 'notfound.html')


def to_notfound(request):
    print '%s redirect_to notfound' % request.path
    return HttpResponseRedirect('/notfound')
