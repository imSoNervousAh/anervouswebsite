from django.shortcuts import render
from django.http import HttpResponseRedirect

def home(request):
	return render(request,'home.html')

def login(request):
	print 'login/'
	if (request.method=='POST'):
		return HttpResponseRedirect('/student')		

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
