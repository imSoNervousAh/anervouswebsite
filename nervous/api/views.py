# -*-coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from database import backend, utils
from api.info_login import auth_by_info as tsinghua_login
import json

def check_student(username, password):
    return tsinghua_login(username, password)

def check_administrator(username, password):
    return backend.check_admin(username, password)

def check_superuser(username, password):
    return (username == 'root') and (password == '123456')


def login(request,identity):
    print 'identity: ',identity
    username, password = request.POST['account'], request.POST['password']
    if (identity in ['student', 'administrator', 'superuser']):
        if (globals()['check_%s' % identity](username, password)):
            return HttpResponseRedirect('/%s' % identity)
        else:
            return render(request, 'login/index.html', {'identity': identity})
    else:
        return HttpResponseRedirect('/index')


def administrator_list(request):
    list = []
    user1 = {}
    user2 = {}
    user1['account'] = 'huangdada'
    user1['password'] = 'keke'
    user2['account'] = 'hucongcong'
    user2['password'] = '123455'
    list.append(user1)
    list.append(user2)
    return HttpResponse(json.dumps(list, sort_keys=True, indent=4, separators=(',', ': ')))


def submit_application(request):
    backend.add_application(request.POST)
    return HttpResponse(request.POST)
    # return HttpResponseRedirect('/student')


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
