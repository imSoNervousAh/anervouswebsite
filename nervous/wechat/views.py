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
        response=render(request, 'login/index.html', {'identity': 'student'})
        return response
    if identity == 'administrator':
        response=  render(request, 'login/index.html', {'identity': 'administrator'})
        return response
    if identity == 'superuser':
        response = render(request, 'login/index.html', {'identity': 'superuser'})
        return response
    return to_notfound(request)

def logout(request):
    identity=session.get_identity(request)
    if identity!='none':
        print 'logout success!'
        session.del_session(request)
        response = login(request,identity)
        return response
    print 'no cookies & logout success!'
    return login(request,'student')

def student(request):
    print 'student identity: ',session.get_identity(request)
    if session.get_identity(request)!='student':
        return login(request,'student')
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

    applications = backend.get_applications()
    #applications  = backend.get_applications_by_user(session.get_username(request))
    for app in applications:
        app.status_glyphicon = glyphicons[app.status]
        app.status_name = status_name[app.status]
    return render(request, 'student/index.html', {'applications': applications,
                                                  'app_count': len(applications),
                                                  'username':session.get_username(request),
                                                  })
    return response

def administrator(request):
    print 'admin identity: ',session.get_identity(request)
    if session.get_identity(request)!=u'administrator':
        return login(request,'administrator')
        
    pending_applications = backend.get_pending_applications()
    #pending_applications = backend.get_pending_applications_by_user()
    official_accounts = backend.get_official_accounts()  
    articles = backend.get_articles()
    return render(request, 'administrator/index.html', {'pending_applications': pending_applications,
                                                        'pending_count': len(pending_applications),
                                                        'official_accounts': official_accounts,
                                                        'account_count': len(official_accounts),
                                                        'articles': articles,
                                                        'article_count': len(articles),
                                                        'username':session.get_username(request),
                                                        })


def detail(request, id):
    try:
        official_account = backend.get_official_account_by_id(id)
    except:
        return to_notfound(request)
    # official_account = {'id': 1234,
    #                     'name': '中老年生活',
    #                     'wechat_id': 'gh_8b162c65a210',
    #                     'subscribers': 128984,
    #                     'description': '让你的中老年生活充满精彩。',
    #                     'association': '离退休办',
    #                     'manager_name': '杨基龙',
    #                     'manager_stu_id': '2014011xxx',
    #                     'manager_dept': '计算基系',
    #                     'manager_tel': '15252520000',
    #                     'manager_email': 'ytl14@mails.tsinghua.edu.cn',
    #                     }
    articles = backend.get_articles_by_official_account_id(id)
    # articles = [{'title': '100个实用的生活小窍门！快转发给你的朋友！',
    #              'description': '假装这里有一段看上去还比较长的文章概要。。。。。。。。。。。。。。。。。。。',
    #              'avatar_url': r'http://mmsns.qpic.cn/mmsns/Q5vXibYbc6KhPTeuiawvxIibuGVDibmETpBg7GRm5BTZLnlMicNWSlhk2JA/0',
    #              'url': r'http://mp.weixin.qq.com/mp/appmsg/show?__biz=MjM5MzA1MDM2MA%3D%3D&appmsgid=10002980&itemidx=2'
    #                     r'&sign=d3b27498589148de49cce5e58313801c&scene=2&from=timeline&isappinstalled=0&uin=MjgzNzgwMzU'
    #                     r'0MQ%3D%3D&key=a45a7c15a542fe6f2ca198c1c45816cce907bfeaa03a6bf0f79c9f8e7713ff0f81fedc195433d44'
    #                     r'475cb136a0227de84&devicetype=android-16&version=25000105&lang=en',
    #              'likes': 1234567,
    #              'views': 21378218
    #              },
    #             {'title': '太吃惊了！手机还可以这么用！',
    #              'description': '你每天都在用手机，但你知道你的手机有什么隐藏功能吗？\n不看不知道！为了你的家人朋友，赶快转发到朋友圈！',
    #              'avatar_url': r'http://mmbiz.qpic.cn/mmbiz/yZPTcMGWibvspeDf9GMv6QIicRDqdiaXuLRiaiaSKUcy9dKHwSeMpbx1s8p'
    #                            r'QlTP9XMu092OmcahIVnI3Z9jQlyXfXyA/0?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1',
    #              'url': r'http://mp.weixin.qq.com/s?__biz=MzA5NDc1NzQ4MA==&mid=208839858&idx=1&sn=9a210da2c8b8bb212444b'
    #                     r'ea4b5b0abea&scene=0&key=2877d24f51fa53848ef8f13923804fb53f0edc80a6f01604b73bca8bace5ddc716d49'
    #                     r'04ffe614ffb8080126af0fbeeb8&ascene=0&uin=MTQ3MDQ0NDI4MA%3D%3D&devicetype=iMac+MacBookPro11%2C'
    #                     r'5+OSX+OSX+10.11+build(15A284)&version=11020201&pass_ticket=TvE7gBRGa%2BQcXPTLSif4hyr8p2u7x46t'
    #                     r'%2BqXjZYNIxgrf0ItimaEdEDtJR0dHNt57',
    #              'likes': 12734,
    #              'views': 973272
    #              }]
    return render(request, 'administrator/detail.html', {'account': official_account,
                                                         'articles': articles,
                                                         'article_count': len(articles),
                                                         })

def superuser(request):
    if session.get_identity(request)!='superuser':
        return login(request,'superuser')
    administrators = backend.get_admins()
    return render(request, 'superuser/index.html', {'administrators': administrators,
                                                    })


def notfound(request):
    print '[in] notfound'
    return render(request, 'notfound.html')


def to_notfound(request):
    print '%s redirect_to notfound' % request.path
    return HttpResponseRedirect('/notfound')
