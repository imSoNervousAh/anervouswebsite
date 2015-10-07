from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import re  
import urllib2  
import urllib  
import cookielib  
import codecs  
import json

def postToApi(myurl,mydata):
	# connect={'sid','s%3AuGZU_VeCrixsynOBkdFSyRbmGSNckCs5.%2F%2BvP0uWNiMTeKdpg22YvEvPc5vXY2o80yMkuLbU7gFQ'}
	# #loginparams = {'connect':connect}  
 #    headers={
 #    	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36',
 #    	'Cookie':'connect.sid=s%3AuGZU_VeCrixsynOBkdFSyRbmGSNckCs5.%2F%2BvP0uWNiMTeKdpg22YvEvPc5vXY2o80yMkuLbU7gFQ',
 #    	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 #    	'Referer':'https://a.n9.vc/group/class20142',
 #    }
 #    data={
 #    	'account':'manager',
 #    	'password':'123456'
 #   	}
   	data=urllib.urlencode(mydata)
   	#request = urllib2.Request(myurl, headers=headers,data=data)    
   	request = urllib2.Request(myurl)    
   	response = urllib2.urlopen(request)
   	return response.read()          
        

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
	str=postToApi("api/managerList","")
	#print str
	#return render(request,'supermanager.html')
	return HttpResponse(str)

def notfound(request):
	print '[in] notfound'
	return render(request,'notfound.html')

def to_notfound(request):
	print '%s redirectto notfound' %request.path
 	#return HttpResponsesRedirect('http://www.baidu.com')
	#return redirect('/notfound/', permanent=True)
 	return HttpResponseRedirect('/notfound')
