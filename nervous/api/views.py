from django.shortcuts import render
from django.http import HttpResponseRedirect


def login(request):
	if (request.POST['account']=='manager') and (request.POST['password']=='123456'):
		return HttpResponseRedirect('/manager')

	if request.POST['account']=='student':
		return HttpResponseRedirect('/student')
	
	if request.POST['account']=='supermanager':
		return HttpResponseRedirect('/supermanager')
	
	return HttpResponseRedirect('/login')
	