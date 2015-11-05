# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import timezone
from datetime import timedelta
from database import backend
from wechat import session
import re
import urllib2
import urllib
import cookielib
import codecs
import json


# misc

def notfound(request):
    print '[in] notfound'
    return render(request, 'notfound.html')


def to_notfound(request):
    print '%s redirect_to notfound' % request.path
    return HttpResponseRedirect('/notfound')


def get_pagination(item_total, item_per_page, cur):
    page_count = (item_total + item_per_page + 1) // item_per_page
    l = max(1, cur - 1)
    r = min(page_count, cur + 2)
    if l <= 2:
        l = 1
    if r >= page_count - 1:
        r = page_count
    pages = xrange(l, r + 1)
    page = {'count': page_count,
            'current': cur,
            'pages': pages}
    return page


# index

def index(request):
    # 默认返回学生登录界面
    return render(request, 'login/index.html', {'identity': 'student'})


def render_ajax(request, url, params):
    if request.is_ajax():
        url = url.split('.')[0] + ".ajax.html"
    else:
        params['username'] = session.get_username(request)

    return render(request, url, params)


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


# student

# decorator for check student fill the basic info
def check_have_student_info(func):
    def wrapper(request, *args, **kw):
        student_id = session.get_username(request)
        if not backend.check_student_information_filled(student_id):
            return student_fill_info(request)
        return func(request, *args, **kw)

    return wrapper


# [ATTENTION]put this decorator at the most previous,decorator for check login status
def check_identity(identity):
    def decorator(func):
        def wrapper(request, *args, **kw):
            if session.get_identity(request) != identity:
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
    student = backend.get_student_by_id(username)
    for app in approved_applications:
        if app.user_submit == username:
            official_accounts.append(app.official_account)

    return render(request, 'student/index.html', {'username': student.real_name,
                                                  'official_accounts': official_accounts,
                                                  'student': student,
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

    return render_ajax(request, 'student/show_applications.html', {'applications': applications,
                                                                   'pending_count': pending_count,
                                                                   })


@check_identity('student')
@check_have_student_info
def student_add_applications(request):
    username=session.get_username(request)
    student = backend.get_student_by_id(username)
    return render_ajax(request, 'student/add_applications.html', {'student':student,
                                                                  'student_id':username,})


@check_identity('student')
def student_fill_info(request):
    return render(request, 'student/info.html', {'type': 'fill',
                                                 'username': '未登录', })


def student_change_info(request):
    identity = session.get_identity(request)
    if identity == 'student':
        username = session.get_username(request)
        student = backend.get_student_by_id(username)
        return render(request, 'student/info.html', {'type': 'change',
                                                     'username': student.real_name,
                                                     'student': student,
                                                     })
    else:
        return HttpResponse(request, '还没有写...')


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
    articles_count, articles = backend.get_articles(sortby=SortBy.Views, filter={
        'posttime_begin': timezone.now().date() - timedelta(days=7)})
    messages = backend.get_messages(only_unprocessed=True)
    return render_ajax(request, 'administrator/dashboard.html', {'pending_applications': pending_applications,
                                                                 'official_accounts': official_accounts,
                                                                 'articles': articles,
                                                                 'articles_count': articles_count,
                                                                 'messages': messages,
                                                                 })


@check_identity('administrator')
def admin_show_official_accounts(request):
    official_accounts = backend.get_official_accounts()

    return render_ajax(request, 'administrator/official_accounts.html', {'official_accounts': official_accounts})


@check_identity('administrator')
def admin_show_articles(request):
    articles_count, articles = backend.get_articles()

    return render_ajax(request, 'administrator/articles.html', {'articles': articles,
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

    return render_ajax(request, 'administrator/applications.html', {'applications': applications,
                                                                    'application_type': type_name,
                                                                    })


@check_identity('administrator')
def admin_show_official_account_detail(request, id):
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    articles_count, articles = backend.get_articles(filter={'official_account_id': id})

    return render_ajax(request, 'administrator/detail.html', {'account': official_account,
                                                              'official_account_id': id,
                                                              'articles_count': articles_count,
                                                              })


@check_identity('administrator')
def admin_show_official_account_articles(request, id):
    articles_on_one_page = 10
    page_current = int(request.GET.get('page', '1'))

    sort_order_keyword = request.GET.get('sort_order', 'desc')
    sort_order = {
        'asc': SortOrder.Ascending,
        'desc': SortOrder.Descending
    }[sort_order_keyword]

    sort_by_keyword = request.GET.get('sort_by', 'posttime')
    sort_by = {
        'posttime': SortBy.Time,
        'likes': SortBy.Likes,
        'views': SortBy.Views
    }[sort_by_keyword]

    article_filter = {}
    keyword = request.GET.get('article_title_keyword', '').strip()
    if keyword:
        article_filter['article_title_keyword'] = keyword
    article_filter['official_account_id'] = id

    articles_count, articles = backend.get_articles(start_from=(page_current - 1) * articles_on_one_page,
                                                    count=articles_on_one_page,
                                                    filter=article_filter,
                                                    sortby=sort_by,
                                                    order=sort_order)

    page = get_pagination(articles_count, articles_on_one_page, page_current)

    return render(request, 'administrator/detail_articles_list.html',
                  {'articles': articles,
                   'articles_count': articles_count,
                   'official_account_id': id,
                   'page': page,
                   'sort_by': sort_by_keyword,
                   'sort_order': sort_order_keyword
                   })


# message

@check_identity('administrator')
def message_detail_admin(request, id):
    category = MessageCategory.ToStudent
    print 'detail'
    messages = backend.get_messages(official_account_id=id)
    print messages[1].processed
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    return render_ajax(request, 'message/message.html', {'account': official_account,
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

    return render_ajax(request, 'message/message.html', {'account': official_account,
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

    return render_ajax(request, 'superuser/admins.html', {'administrators': administrators})
