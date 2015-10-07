from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json

def login(request):
	if (request.POST['account']=='manager') and (request.POST['password']=='123456'):
		return HttpResponseRedirect('/manager')

	if request.POST['account']=='student':
		return HttpResponseRedirect('/student')
	
	if request.POST['account']=='supermanager':
		return HttpResponseRedirect('/supermanager')
	
	return HttpResponseRedirect('/login')

def managerList(requesr):
	list=[]
	user1={} 
	user1['account']='huangdada'
	user1['password']='keke'
	user2['account']='hucongcong'
	user2['password']='123455'
	list.append(user1)
	list.append(user2)
	return HttpResponse(json.dumps(list))	