from django.shortcuts import render

def home(request):
	return render(request,'home.html')

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
	print 'jump to notfound...'
	return render(request,'notfound.html')

def to_notfound(request):
	#print '%s redirectto notfound' %request.path
	return HttpResponseRedirect('/notfound')
