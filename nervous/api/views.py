# -*-coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from database import backend, utils
from api.info_login import auth_by_info as tsinghua_login
import json

from wechat import session


def check_student(username, password):
    return tsinghua_login(username, password)


def check_administrator(username, password):
    return backend.check_admin(username, password)


def check_superuser(username, password):
    return (username == 'root') and (password == '123456')


def login(request, identity):
    print 'identity: ', identity
    username, password = request.POST['account'], request.POST['password']
    if identity in ['student', 'administrator', 'superuser']:
        if globals()['check_%s' % identity](username, password):
            session.add_session(request, identity=identity, username=username)
            response = HttpResponseRedirect('/%s' % identity)
            return response
        else:
            response = render(request, 'login/index.html', {'identity': identity})
            session.del_session(request)
            return response
    else:
        response = HttpResponseRedirect('/index')
        session.del_session(request)
        return response


def submit_application(request):
    dic = request.POST.dict()
    print dic
    username = session.get_username(request)
    print "submit_application", username
    dic['user_submit'] = username
    backend.add_application(dic)
    return HttpResponse(request.POST)


def modify_application(request):
    backend.modify_application(request.POST)
    return HttpResponseRedirect('/administrator')


def add_admin(request):
    backend.add_admin(request.POST['username'], request.POST['password'], request.POST['description'])
    return HttpResponseRedirect('/superuser')


def del_admin(request):
    print "del %s" % request.POST['username']
    backend.del_admin(request.POST['username'])
    return HttpResponseRedirect('/superuser')

def add_message(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    backend.add_message(
           dic['category'],
           dic['official_account_id'],
           dic['title'],
           dic['content'],
           username
    )
    print dic['category'],' ',MessageCategory.ToStudent
    if (dic['category'] == str(MessageCategory.ToStudent)):
        print 'add message admin'
        return HttpResponseRedirect('/administrator/message/%s' % dic['official_account_id'])
    else:
        print 'add message student'
        return HttpResponseRedirect('/student/message/%s' % dic['official_account_id'])
