#-*-coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json

def login(request,identity):
	#check student login
	if (identity=='student'):
		if (request.POST['account']=='hzc') and (request.POST['password']=='123456'):
			return HttpResponseRedirect('/administrator')
		else: 	
			return render(request,'login/index.html',{'identity':'student'})
	
	#check administrator login
	if (identity=='administrator'):
		if (request.POST['account']=='admin') and (request.POST['password']=='123456'):
			return HttpResponseRedirect('/student')
		else:
			return render(request,'login/index.html',{'identity':'administrator'})

	#check superuser login
	if (identity=='superuser'):
		if (request.POST['account']=='root') and (request.POST['password']=='123456'):
			return HttpResponseRedirect('/superuser')
		else:
			return render(request,'login/index.html',{'identity':'superuser'})
	
	return HttpResponseRedirect('/index')

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
