# -*-coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from database import backend, utils
import json


def login(request):
    print 'account: ', request.POST['account'], ' password: ', request.POST['password']
    if request.POST['account'] == 'administrator':
        return HttpResponseRedirect('/administrator')

    if request.POST['account'] == 'student':
        return HttpResponseRedirect('/student')

    if request.POST['account'] == 'superuser':
        return HttpResponseRedirect('/superuser')

    return HttpResponseRedirect('/login')


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
    return HttpResponseRedirect('/student')


def add_admin(request):
    backend.add_admin(request.POST)
    return HttpResponseRedirect('/superuser')


def del_admin(request):
    backend.del_admin(request.POST)
    return HttpResponseRedirect('/superuser')
