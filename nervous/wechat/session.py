def add_session(request,*args,**kw):
	#request.session.set_expiry()
	print 'add_session: ',kw
	for (key,value) in kw.items():
		request.session[key]=value

def del_session(request):
	try:
		del request.session['username']
		del request.session['identity']    
	except KeyError:
		pass

def get_username(request):
	if (request.session.has_key('username')):
		return request.session['username']
	return 'none'

def get_identity(request):
	if (request.session.has_key('identity')):
		return request.session['identity']
	return 'none'

