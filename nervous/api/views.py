# -*-coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from database import backend, utils
import json


def login(request, identity):
    print 'identity: ', identity
    # check student login
    if (identity == 'student'):
        if (request.POST['account'] == 'hzc') and (request.POST['password'] == '123456'):
            return HttpResponseRedirect('/student')
        else:
            return render(request, 'login/index.html', {'identity': 'student'})

    # check administrator login
    if (identity == 'administrator'):
        if (request.POST['account'] == 'admin') and (request.POST['password'] == '123456'):
            return HttpResponseRedirect('/administrator')
        else:
            return render(request, 'login/index.html', {'identity': 'administrator'})

    # check superuser login
    if (identity == 'superuser'):
        if (request.POST['account'] == 'root') and (request.POST['password'] == '123456'):
            return HttpResponseRedirect('/superuser')
        else:
            return render(request, 'login/index.html', {'identity': 'superuser'})

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
