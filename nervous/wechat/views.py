from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

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
	#now = datetime.datetime.now()
	t = get_template('supermanager/index.html')
	#html = t.render(Context({'current_date': now}))
	html=t.render(request)
	return HttpResponse(html)
	#return render(request,'supermanager/index.html')

def notfound(request):
	print '[in] notfound'
	return render(request,'notfound.html')

def to_notfound(request):
	print '%s redirectto notfound' %request.path
 	#return HttpResponsesRedirect('http://www.baidu.com')
	#return redirect('/notfound/', permanent=True)
 	return HttpResponseRedirect('/notfound')
