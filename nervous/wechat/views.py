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

# decorator for check student fill the basic info
def check_have_student_info(func):
    def wrapper(request, *args, **kw):
        if backend.check_student_information_filled(session.get_username(request)) == False:
            return student_fill_student_info(request)
        return func(request, *args, **kw)

    return wrapper


# [ATTENTION]put this decorator at the most previous,decorator for check login status
def check_identity(identity):
    def decorator(func):
        def wrapper(request, *args, **kw):
            if (session.get_identity(request) != identity):
                return login(request, identity)
            return func(request, *args, **kw)

        return wrapper

    return decorator


@check_identity('student')
@check_have_student_info
def student(request):
    username = session.get_username(request)

    approved_applications = backend.get_applications_by_status('approved')
    official_accounts = []
    for app in approved_applications:
        if app.user_submit == username:
            official_accounts.append(app.official_account)

    return render(request, 'student/index.html', {'username': username,
                                                  'official_accounts': official_accounts,
                                                  })


@check_identity('student')
@check_have_student_info
def student_show_applications(request):
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


@check_identity('student')
@check_have_student_info
def student_add_applications(request):
    return render(request, 'student/add_applications.html', {})


def student_fill_student_info(request):
    print 'fill_basic_info'
    return render(request, 'student/fill_student_info.html')


@check_identity('student')
def student_fill_student_info(request):
    print 'fill_basic_info'
    return render(request, 'student/fill_student_info.html')


# administrator
@check_identity('administrator')
def admin(request):
    print 'show admin'

    pending_applications_count = len(backend.get_pending_applications())
    username = session.get_username(request)

    return render(request, 'administrator/index.html', {'username': username,
                                                        'pending_applications_count': pending_applications_count})


@check_identity('administrator')
def admin_dashboard(request):
    pending_applications = backend.get_pending_applications()
    official_accounts = backend.get_official_accounts()
    articles_count, articles = backend.get_articles()
    messages = backend.get_messages(only_unprocessed=True)

    return render(request, 'administrator/dashboard.html', {'pending_applications': pending_applications,
                                                            'official_accounts': official_accounts,
                                                            'articles': articles,
                                                            'articles_count': articles_count,
                                                            'messages': messages,
                                                            })


@check_identity('administrator')
def admin_show_official_accounts(request):
    official_accounts = backend.get_official_accounts()

    return render(request, 'administrator/official_accounts.html', {'official_accounts': official_accounts})


@check_identity('administrator')
def admin_show_articles(request):
    articles_count, articles = backend.get_articles()

    return render(request, 'administrator/articles.html', {'articles': articles,
                                                           'articles_count': articles_count,
                                                           })


@check_identity('administrator')
def admin_show_applications(request, type):
    if type == 'pending':
        applications = backend.get_pending_applications()
        type_name = u'待审批申请'
    elif type == 'processed':
        username = session.get_username(request)
        applications = backend.get_applications_by_admin(username)
        type_name = u'我处理的申请'
    elif type == 'all':
        applications = backend.get_applications()
        type_name = u'所有申请'
    else:
        applications = []
        type_name = ''

    return render(request, 'administrator/applications.html', {'applications': applications,
                                                               'application_type': type_name,
                                                               })


@check_identity('administrator')
def admin_show_official_account_detail(request, id):
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    articles_count = backend.get_articles()

    return render(request, 'administrator/detail.html', {'account': official_account,
                                                         'official_account_id': id,
                                                         'articles_count': articles_count,
                                                         })


@check_identity('administrator')
def admin_show_official_account_articles(request, id):
    articles_on_one_page = 10
    page_current = int(request.GET.get('page', '1'))
    sort_order = {
        'asc': SortOrder.Ascending,
        'desc': SortOrder.Descending
    }[request.GET.get('sort_order', 'asc')]
    sort_by = {
        'time': SortBy.Time,
        'likes': SortBy.Likes,
        'views': SortBy.Views
    }[request.GET.get('sort_by', 'time')]

    articles_count, articles = backend.get_articles(start_from=(page_current - 1) * articles_on_one_page,
                                                    count=articles_on_one_page,
                                                    filter={'official_account_id': id},
                                                    sortby=sort_by,
                                                    order=sort_order)

    page_count = (articles_count + articles_on_one_page - 1) // articles_on_one_page
    pages = xrange(1, page_count + 1)
    page = {'count': page_count,
            'current': page_current,
            'pages': pages}

    return render(request, 'administrator/detail_articles_list.html',
                  {'articles': articles,
                   'official_account_id': id,
                   'page': page,
                   'sort_by': request.GET.get('sort_by', 'time'),
                   'sort_order': request.GET.get('sort_order', 'asc')
                   })


# message


@check_identity('administrator')
def message_detail_admin(request, id):
    category = MessageCategory.ToStudent

    messages = backend.get_messages(official_account_id=id)
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    return render(request, 'message/message.html', {'account': official_account,
                                                    'messages': messages,
                                                    'category': category,
                                                    'official_account_id': id,
                                                    })


@check_identity('student')
def message_detail_student(request, id):
    category = MessageCategory.ToAdmin
    messages = backend.get_messages(official_account_id=id)
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    return render(request, 'message/message.html', {'account': official_account,
                                                    'messages': messages,
                                                    'category': category,
                                                    'official_account_id': id,
                                                    })


# superuser

@check_identity('superuser')
def superuser(request):
    return render(request, 'superuser/index.html', {'username': u'超级管理员'})


@check_identity('superuser')
def superuser_show_admins(request):
    administrators = backend.get_admins()

    return render(request, 'superuser/admins.html', {'administrators': administrators})


# misc

def notfound(request):
    print '[in] notfound'
    return render(request, 'notfound.html')


def to_notfound(request):
    print '%s redirect_to notfound' % request.path
    return HttpResponseRedirect('/notfound')
