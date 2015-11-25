# identity=['student','admin','superuser']


def add_session(request, *args, **kw):
    # request.session.set_expiry()
    print 'add_session: ', kw
    for (key, value) in kw.items():
        request.session[key] = value


def del_session(request):
    try:
        del request.session['username']
        del request.session['identity']
    except KeyError:
        pass


def get_username(request):
    if 'username' in request.session:
        return request.session['username']
    return 'none'


def get_identity(request):
    if 'identity' in request.session:
        return request.session['identity']
    return 'none'
