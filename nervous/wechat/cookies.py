import json

def check_cookies_from_request(request,identity):
    cookies_str = request.COOKIES.get('mycookies','')
    if cookies_str:
        mycookies=json.loads(cookies_str)
        return mycookies['identity']==identity
    return False

def get_identity_from_request(request):
    cookies_str = request.COOKIES.get('mycookies','')
    if cookies_str:
        mycookies=json.loads(cookies_str)
        return mycookies['identity']
    return 'none'

def get_username_from_request(request):
    cookies_str = request.COOKIES.get('mycookies','')
    if cookies_str:
        mycookies=json.loads(cookies_str)
        return mycookies['username']
    return 'none'

def get_cookies_from_request(request):
    cookies_str = request.COOKIES.get('mycookies','')
    if cookies_str:
        mycookies=json.loads(cookies_str)
        return mycookies
    return {'identity':'none','username':'none'}

def make_cookies_from_response(response,identity,username):
            
    mycookies={}
    mycookies['identity']=identity
    mycookies['username']=username
    response.set_cookie('mycookies',json.dumps(mycookies),3600)
    return response

def delete_cookies_from_response(response):
    response.delete_cookie('mycookies')
    return response
            
            
