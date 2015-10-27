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


def index(request):
    # 默认返回学生登录界面
    return render(request, 'login/index.html', {'identity': 'student'})


def login(request, identity='student'):
    print 'login/'
    if identity == 'student':
        response = render(request, 'login/index.html', {'identity': 'student'})
        return response
    if identity == 'administrator':
        response = render(request, 'login/index.html', {'identity': 'administrator'})
        return response
    if identity == 'superuser':
        response = render(request, 'login/index.html', {'identity': 'superuser'})
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


def student(request):
    print 'student identity: ', session.get_identity(request)
    if session.get_identity(request) != 'student':
        return login(request, 'student')
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

    username = session.get_username(request)
    applications  = backend.get_applications_by_user(username)
    pending_count = 0
    for app in applications:
        app.status_glyphicon = glyphicons[app.status]
        app.status_name = status_name[app.status]
        if app.status == 'pending':
            pending_count += 1

    return render(request, 'student/index.html', {'applications': applications,
                                                  'pending_count': pending_count,
                                                  'username': session.get_username(request),
                                                  })


def administrator(request):
    print 'admin identity: ', session.get_identity(request)
    if session.get_identity(request) != u'administrator':
        return login(request, 'administrator')

    pending_applications = backend.get_pending_applications()
    # pending_applications = backend.get_pending_applications_by_user()
    official_accounts = backend.get_official_accounts()
    articles = backend.get_articles()

    return render(request, 'administrator/index.html', {'pending_applications': pending_applications,
                                                        'official_accounts': official_accounts,
                                                        'articles': articles,
                                                        'username': session.get_username(request),
                                                        })


def detail(request, id):
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)
    articles = backend.get_articles_by_official_account_id(id)

    return render(request, 'administrator/detail.html', {'account': official_account,
                                                         'articles': articles,
                                                         'article_count': len(articles),
                                                         'username': session.get_username(request),
                                                         })


def superuser(request):
    if session.get_identity(request) != 'superuser':
        return login(request, 'superuser')
    administrators = backend.get_admins()
    return render(request, 'superuser/index.html', {'administrators': administrators,
                                                    'username': u'超级管理员',
                                                    })


def notfound(request):
    print '[in] notfound'
    return render(request, 'notfound.html')


def to_notfound(request):
    print '%s redirect_to notfound' % request.path
    return HttpResponseRedirect('/notfound')
