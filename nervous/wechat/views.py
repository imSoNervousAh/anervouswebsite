from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

def index(request):
	return render(request,'login.html')

def login(request):
	print 'login/'
	return render(request,'login.html')

def student(request):
	return render(request,'student.html')

def manager(request):
	return render(request,'manager.html')

def supermanager(request):
	return render(request,'supermanager.html')

def notfound(request):
	print '[in] notfound'
	return render(request,'notfound.html')

def to_notfound(request):
	print '%s redirectto notfound' %request.path
 	#return HttpResponsesRedirect('http://www.baidu.com')
	#return redirect('/notfound/', permanent=True)
 	return HttpResponseRedirect('/notfound')
