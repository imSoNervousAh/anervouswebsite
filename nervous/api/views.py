#-*-coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json

def login(request):
	print 'account: ',request.POST['account'],' password: ',request.POST['password']
	if (request.POST['account']=='administrator'):
		return HttpResponseRedirect('/administrator')

	if request.POST['account']=='student':
		return HttpResponseRedirect('/student')
	
	if request.POST['account']=='superuser':
		return HttpResponseRedirect('/superuser')
	
	return HttpResponseRedirect('/login')

def managerList(request):
	list=[]
	user1={} 
	user1['account']='huangdada'
	user1['password']='keke'
	user2['account']='hucongcong'
	user2['password']='123455'
	list.append(user1)
	list.append(user2)
	return HttpResponse(json.dumps(list, sort_keys=True,  indent=4, separators=(',', ': ')))

def submit_application(request):
	return HttpResponse(json.dumps(request.POST, sort_keys=True, indent=4, separators=(',', ': ')))
