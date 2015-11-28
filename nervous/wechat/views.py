# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from database import backend
from database.models import *
from wechat import session


# misc

def notfound(request):
    print '[in] notfound'
    return render(request, 'notfound.html')


def to_notfound(request):
    print '%s redirect_to notfound' % request.path
    return HttpResponseRedirect('/notfound')


def get_pagination(item_total, item_per_page, cur):
    page_count = (item_total + item_per_page - 1) // item_per_page

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


def render_sortable(request, items, url, params=None):
    if not params:
        params = {}
    items_per_page = params.pop("items_per_page", 10)

    page_current = int(request.GET.get('page', '1'))

    sort_order_keyword = request.GET.get('sort_order', 'desc')
    sort_order = {
        'asc': '',
        'desc': '-'
    }[sort_order_keyword]

    sort_by_keyword = request.GET.get('sort_by', '')

    set_filter = {}
    search_keyword = request.GET.get('search_keyword', '').strip()
    search_field = request.GET.get('search_field')
    if search_field and search_keyword:
        set_filter[search_field + '__contains'] = search_keyword

    start_from = (page_current - 1) * items_per_page

    items = items.filter(**set_filter).order_by(sort_order + sort_by_keyword)
    item_count = items.count()
    items = items[start_from:(start_from + items_per_page)]

    page = get_pagination(item_count, items_per_page, page_current)

    return render(request, url, {
        'items': items,
        'item_count': item_count,
        'page': page,
        'sort_by': sort_by_keyword,
        'sort_order': sort_order_keyword,
        'params': params
    })


def get_realname(request):
    username = session.get_username(request)
    identity = session.get_identity(request)
    if identity == 'student':
        realname = backend.get_student_by_id(username).real_name
    else:
        realname = username
    return realname


# index

def index(request):
    identity = session.get_identity(request)
    if identity == 'none':
        return login(request)
    elif identity == 'student':
        return student(request)
    elif identity == 'admin':
        return admin(request)
    elif identity == 'superuser':
        return superuser(request)
    else:
        return notfound(request)


def render_ajax(request, url, params, item_id=''):
    if request.is_ajax():
        url = '.'.join(url.split('.')[:-1]) + '.ajax.html'
    else:
        identity = session.get_identity(request)
        name = get_realname(request)
        params['username'] = name
        if item_id != '':
            params['active_item'] = item_id
        if identity == 'admin':
            params['pending_applications_count'] = len(backend.get_pending_applications())
        elif identity == 'student':
            username = session.get_username(request)
            applications = backend.get_applications_by_user(username)
            official_accounts = applications.filter(status__exact='approved')
            params['official_accounts'] = official_accounts

    return render(request, url, params)


# login/logout

def login(request):
    return render(request, 'login.html')


def logout(request):
    identity = session.get_identity(request)
    if identity != 'none':
        print 'logout success!'
        session.del_session(request)
    print 'no cookies & logout success!'
    return HttpResponseRedirect('/login')


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
                if request.is_ajax():
                    return HttpResponseForbidden()
                else:
                    return HttpResponseRedirect('/login')
            return func(request, *args, **kw)

        return wrapper

    return decorator


# home
def home(request):
    identity = session.get_identity(request)
    if identity in ['student', 'admin', 'superuser']:
        return HttpResponseRedirect('/%s' % identity)

    return login(request)


@check_identity('student')
def change_info(request):
    username = session.get_username(request)
    student = backend.get_student_by_id(username)
    return render(request, 'student/info.html', {
        'type': 'change',
        'username': student.real_name,
        'student': student,
    })


@check_identity('student')
@check_have_student_info
def student(request):
    return student_show_applications(request)


@check_identity('student')
@check_have_student_info
def student_show_applications(request):
    username = session.get_username(request)
    applications = backend.get_applications_by_user(username)

    return render_ajax(request, 'student/show_applications.html', {
        'applications': applications,
    }, 'my-applications-item')


@check_identity('student')
@check_have_student_info
def student_add_applications(request):
    username = session.get_username(request)
    student = backend.get_student_by_id(username)
    return render_ajax(request, 'student/modify_applications.html', {
        'student': student,
        'student_id': username,
        'username': student.real_name,
    }, 'add-application-item')


@check_identity('student')
@check_have_student_info
def student_modify_applications(request, id):
    username = session.get_username(request)
    student = backend.get_student_by_id(username)
    app = backend.get_application_by_id(id)
    print 'in student_modify_applications..'
    print 'real_name is:', student.real_name
    return render_ajax(request, 'student/modify_applications.html', {
        'student': student,
        'student_id': username,
        'username': student.real_name,
        'app': app,
        'modify_app': 'true',
    })


@check_identity('student')
def student_fill_info(request):
    return render(request, 'student/info.html', {
        'type': 'fill',
        'username': '未登录'
    })


@check_identity('student')
@check_have_student_info
def student_change_info(request):
    username = session.get_username(request)
    student = backend.get_student_by_id(username)
    return render(request, 'student/info.html', {
        'type': 'change',
        'username': student.real_name,
        'student': student,
        'unprocessed_category': MessageCategory.ToStudent,
    })


@check_identity('student')
def student_badge_pending_count(request):
    username = session.get_username(request)
    applications = backend.get_applications_by_user(username)
    pending_count = applications.filter(status__exact='pending').count()
    return HttpResponse(pending_count)


@check_identity('student')
def student_badge_account_unprocessed_message_count(request, id):
    account = backend.get_official_account_by_id(id)
    message_count = account.unprocessed_messages_count(MessageCategory.ToStudent)
    if message_count == 0:
        return HttpResponse()
    return HttpResponse(message_count)


# admin
@check_identity('admin')
def admin(request):
    print 'show admin'

    return admin_dashboard(request)


@check_identity('admin')
def admin_dashboard(request):
    pending_applications = backend.get_pending_applications()
    pending_count = pending_applications.count()
    show_all_pending_applications = False
    if pending_count > 10:
        show_all_pending_applications = True
        pending_applications = pending_applications[0:10]
    official_accounts = backend.get_official_accounts().order_by('-wci')[0:10]
    articles_count, articles = backend.get_articles(sortby=SortBy.Views, filter={
        'posttime_begin': timezone.now().date() - timedelta(days=7)
    })
    category = MessageCategory.ToAdmin
    unprocessed_account = backend.get_official_accounts_with_unprocessed_messages(category)
    announcement = backend.get_announcement()
    return render_ajax(request, 'admin/dashboard.html', {
        'pending_applications': pending_applications,
        'official_accounts': official_accounts,
        'articles': articles,
        'articles_count': articles_count,
        'unprocessed_account': unprocessed_account,
        'category': category,
        'announcement': announcement,
        'show_all_pending_applications': show_all_pending_applications
    }, 'dashboard-item')


@check_identity('admin')
def admin_show_official_accounts(request):
    return render_ajax(request, 'admin/official_accounts/official_accounts.html', {
    }, 'official-accounts-list-item')


@check_identity('admin')
def admin_show_official_accounts_list(request, folder):
    return render_sortable(request, backend.get_official_accounts(),
                           'admin/' + folder + '/official_accounts_content.html')


@check_identity('admin')
def admin_show_statistics(request):
    official_accounts = backend.get_official_accounts()

    return render_ajax(request, 'admin/statistics/statistics.html', {
        'official_accounts': official_accounts
    }, 'statistics-list-item')


@check_identity('admin')
def admin_show_articles(request):
    return render_ajax(request, 'admin/articles/articles.html', {
    }, 'articles-list-item')


@check_identity('admin')
def admin_show_articles_list(request):
    return render_sortable(request, backend.Article.objects.all(),
                           'admin/articles/articles_content.html')


@check_identity('admin')
def admin_show_applications(request, type):
    if type == 'pending':
        type_name = u'待审批申请'
        type_icon = 'fa-tasks'
    elif type == 'processed':
        type_name = u'我处理的申请'
        type_icon = 'fa-check'
    elif type == 'all':
        type_name = u'所有申请'
        type_icon = 'fa-list-alt'
    else:
        type_name = ''
        type_icon = ''
    item_id = type + '-applications-item'

    return render_ajax(request, 'admin/applications/applications.html', {
        'type': type,
        'application_type': type_name,
        'application_icon': type_icon
    }, item_id)


@check_identity('admin')
def admin_show_applications_list(request, type):
    if type == 'pending':
        applications = backend.get_pending_applications()
    elif type == 'processed':
        username = session.get_username(request)
        applications = backend.get_applications_by_admin(username)
    elif type == 'all':
        applications = backend.get_applications().exclude(status='not_submitted')
    else:
        applications = []
    return render_sortable(request, applications,
                           'admin/applications/applications_content.html', {
                               'type': type
                           })


@check_identity('admin')
def admin_show_official_account_detail(request, id):
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    articles_count, articles = backend.get_articles(filter={'official_account_id': id})

    return render_ajax(request, 'admin/detail/detail.html', {
        'account': official_account,
        'official_account_id': id,
        'articles_count': articles_count,
    })


@check_identity('admin')
def admin_show_official_account_statistics(request, id):
    official_account = backend.get_official_account_by_id(id)
    articles = backend.get_articles_by_official_account_id(id)

    records = backend.get_records(id,
                                  timezone.now().date() - timedelta(days=8),
                                  timezone.now().date())
    records = records.order_by('date')

    def get_oa_chart_json():
        chart_data = {
            'chart': {
                'caption': '公众号一周信息',
                'subCaption': official_account.name,
                'xAxisName': '日期',
                'pYAxisName': '阅读数',
                'sYAxisName': '点赞数',
                'sYAxisMaxValue': int(reduce(lambda x, y: max(x, y.likes),
                                             records, 0) * 0.18) * 10
            },
            'categories': [
                {'category': []}
            ],
            'dataset': [
                {
                    'seriesName': '阅读数',
                    'data': []
                },
                {
                    'seriesName': '点赞数',
                    'parentYAxis': 'S',
                    'renderAs': 'area',
                    'data': []
                }
            ]
        }

        if len(records) == 1:
            chart_data['dataset'][1]['renderAs'] = 'column'

        for x in records:
            chart_data['categories'][0]['category'].append({'label': str(x.date)})
            chart_data['dataset'][0]['data'].append({'value': x.views})
            chart_data['dataset'][1]['data'].append({'value': x.likes})

        chart_json = json.dumps(chart_data)
        return chart_json

    def get_article_views_chart_json():
        chart_data = {
            'chart': {
                'caption': '公众号文章阅读量分类',
                'subCaption': official_account.name,
                'showLegend': '1',
                'legendItemFontSize': '12',
            },
            'data': []
        }

        def add_data(dic):
            if dic['value'] > 0:
                chart_data['data'].append(dic)

        add_data({
            'label': '不超过 200 次',
            'value': articles.filter(views__lte=200).count()
        })
        view_segments = [200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
        for i in xrange(1, len(view_segments)):
            views_l = view_segments[i - 1] + 1
            views_r = view_segments[i]
            count = articles.filter(views__gte=views_l, views__lte=views_r).count()
            add_data({
                'label': '%d ~ %d 次' % (views_l, views_r),
                'value': count
            })
        add_data({
            'label': '100000 次以上',
            'value': articles.filter(views__gt=100000).count()
        })

        chart_json = json.dumps(chart_data)
        return chart_json

    def get_article_likes_chart_json():
        chart_data = {
            'chart': {
                'caption': '公众号文章点赞量分类',
                'subCaption': official_account.name,
                'showLegend': '1',
                'legendItemFontSize': '12',
            },
            'data': []
        }

        def add_data(dic):
            if dic['value'] > 0:
                chart_data['data'].append(dic)

        add_data({
            'label': '不超过 2 次',
            'value': articles.filter(likes__lte=2).count()
        })
        like_segments = [2, 5, 10, 20, 50, 100, 200]
        for i in xrange(1, len(like_segments)):
            likes_l = like_segments[i - 1] + 1
            likes_r = like_segments[i]
            count = articles.filter(likes__gte=likes_l, likes__lte=likes_r).count()
            add_data({
                'label': '%d ~ %d 次' % (likes_l, likes_r),
                'value': count
            })
        add_data({
            'label': '200 次以上',
            'value': articles.filter(likes__gt=200).count()
        })

        chart_json = json.dumps(chart_data)
        return chart_json

    def get_history_chart_json():
        chart_data = {
            'chart': {
                'caption': '公众号一周WCI变化',
                'subCaption': official_account.name,
                'xAxisName': '日期',
                'yAxisName': 'WCI'
            },
            'data': [],
            'trendlines': [
                {
                    'line': [
                        {
                            'startValue': official_account.wci,
                            'displayValue': '当前抓取WCI{br}' + str(round(official_account.wci, 2)),
                            'color': '#1aaf5d',
                            'valueOnRight': '1',
                            'thickness': '2'
                        }
                    ]
                }
            ]
        }

        for x in records:
            chart_data['data'].append({
                'label': str(x.date),
                'value': round(x.wci, 2)
            })

        chart_json = json.dumps(chart_data)
        return chart_json

    return render(request, 'admin/detail/detail_statistics.html', {
        'account': official_account,
        'article_count': articles.count(),
        'oa_chart_json': get_oa_chart_json(),
        'article_views_chart_json': get_article_views_chart_json(),
        'article_likes_chart_json': get_article_likes_chart_json(),
        'history_chart_json': get_history_chart_json()
    })


@check_identity('admin')
def admin_show_official_account_articles(request, id):
    return render(request, 'admin/detail/detail_articles.html', {'official_account_id': id})


@check_identity('admin')
def admin_show_official_account_articles_list(request, id):
    set = backend.get_articles_by_official_account_id(id)
    return render_sortable(request, set,
                           'admin/detail/detail_articles_content.html', {
                               'official_account_id': id
                           })


@check_identity('admin')
def admin_forewarn_rules(request):
    wx_name = map(lambda account: account.name, backend.get_official_accounts())

    return render_ajax(request, 'admin/forewarn/forewarn_rules.html', {}, 'forewarn-rules-item')


@check_identity('admin')
def admin_forewarn_rules_list(request):
    return render_sortable(request, backend.get_forewarn_rules(),
                           'admin/forewarn/forewarn_rules_content.html')


@check_identity('admin')
def admin_show_forewarn_rules_modal(request, type, id=None):
    wx_name = map(lambda account: account.name, backend.get_official_accounts())
    if type == 'modify':
        rule = backend.get_forewarn_rule_by_id(id)
    else:
        rule = None
    print rule
    return render(request, 'admin/forewarn/forewarn_rules_modal.html', {
        'rule': rule,
        'type': type,
        'NotificationOption': NotificationOption,
        'ForewarnTarget': ForewarnTarget,
        'wx_name': wx_name,
    })


@check_identity('admin')
def admin_forewarn_records(request):
    return render_ajax(request, 'admin/forewarn/forewarn_records.html', {
    }, 'forewarn-records-item')


@check_identity('admin')
def admin_forewarn_records_list(request):
    return render_sortable(request, backend.get_forewarn_records(),
                           'admin/forewarn/forewarn_records_content.html', {
                               'items_per_page': 20
                           })


@check_identity('admin')
def admin_show_application_modal(request, type, id):
    application = backend.get_application_by_id(id)
    return render(request, 'admin/application_modal.html', {
        'app': application,
        'type': type
    })


@check_identity('admin')
def admin_badge_pending_count(request):
    pending_count = backend.get_applications_by_status('pending').count()
    return HttpResponse(pending_count)


# message

def message_jump(request, id):
    return HttpResponseRedirect('/message/%s/%s' % (session.get_identity(request), id))


def check_processed(messages, category):
    for message in messages:
        if (message.category != category) and (not message.processed):
            print message
            return False
    return True


@check_identity('admin')
def message_detail_admin(request, id):
    category = MessageCategory.ToStudent
    print 'detail'
    messages = backend.get_messages(official_account_id=id)

    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    return render_ajax(request, 'message/message.html', {
        'account': official_account,
        'messages': messages,
        'category': category,
        'official_account_id': id,
        'processed': check_processed(messages, category),
        'MessageCategory': MessageCategory,
        'locate': 'admin/index.html',
    })


@check_identity('student')
def message_detail_student(request, id):
    category = MessageCategory.ToAdmin
    messages = backend.get_messages(official_account_id=id)
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)

    return render_ajax(request, 'message/message.html', {
        'account': official_account,
        'messages': messages,
        'category': category,
        'official_account_id': id,
        'processed': check_processed(messages, category),
        'MessageCategory': MessageCategory,
        'locate': 'student/index.html'
    }, 'message-detail-' + str(id))


# superuser

@check_identity('superuser')
def superuser(request):
    return superuser_show_admins(request)


@check_identity('superuser')
def superuser_show_admins(request):
    admins = backend.get_admins()

    return render_ajax(request, 'superuser/admins.html', {
        'admins': admins,
        'username': get_realname(request),
    }, 'admins-list-item')


@check_identity('superuser')
def superuser_modify_announcement(request):
    announcement = backend.get_announcement()
    return render_ajax(request, 'superuser/modify_announcement.html', {
        'announcement': announcement,
    }, 'modify-announcement-item')


@check_identity('superuser')
def superuser_manage_database(request):
    def all_count(model):
        return model.objects.all().count()

    count = {}

    themodals = [OfficialAccount, Article, Student, Application, Admin, Message, ForewarnRule, ForewarnRecord]
    for i in range(0, len(themodals)):
        count[themodals[i].__name__] = all_count(themodals[i])

    thestatus = ['approved', 'rejected', 'pending', 'not_submitted']
    for status in thestatus:
        count['application_' + status] = len(backend.get_applications_by_status(status))

    root_name = 'root'

    return render_ajax(request, 'superuser/manage_database.html', {
        'count': count,
        'root_name': root_name,
    }, 'database-info-item')


@check_identity('superuser')
def superuser_update_database(request):
    return render_ajax(request, 'superuser/update_database.html', {
    }, 'update-data-item')


@check_identity('superuser')
def superuser_progress_item(request):
    progress = backend.update_progress()
    updating_account = backend.updating_account_name()
    response = {
        'progress': progress,
        'updating_account': updating_account,
    }
    return JsonResponse(response)


@check_identity('superuser')
def superuser_show_add_admin_modal(request):
    return render(request, 'superuser/add_admin_modal.html')
