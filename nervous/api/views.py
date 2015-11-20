# -*-coding:utf-8

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from api.info_login import auth_by_info as tsinghua_login
from database import backend
from wechat import session
from django.core.exceptions import ValidationError

# Utils

def response_success():
    response = {
        'status': 'ok'
    }
    return response


def response_from_validation_error(e):
    error_dict = e.message_dict
    key, value = error_dict.popitem()
    response = {
        'status': 'error',
        'error_message': value,
        'error_field': key,
    }
    return response

def response_from_exception(e):
    response = {
        'status': 'error',
        'error_message': e.__unicode__(),
    }
    return response


# Views

def check_admin(username, password):
    return backend.check_admin(username, password)


def check_student(username, password):
    return tsinghua_login(username, password) or check_admin(username, password)


def check_superuser(username, password):
    return (username == 'root') and (password == '123456')


def login(request, identity):
    print 'identity: ', identity
    username, password = request.POST['account'], request.POST['password']
    if identity in ['student', 'admin', 'superuser']:
        if globals()['check_%s' % identity](username, password):
            session.add_session(request, identity=identity, username=username)
            response = HttpResponseRedirect('/%s' % identity)
            return response
        else:
            response = render(request, 'login/index.html', {'identity': identity})
            session.del_session(request)
            return response
    else:
        response = HttpResponseRedirect('/index')
        session.del_session(request)
        return response


def submit_student_info(request):
    dic = request.POST.dict()
    print dic
    username = session.get_username(request)
    backend.set_student_information(username, dic)
    print "submit_student_info: ", username," success"
    return HttpResponseRedirect('/student')


def submit_application(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    dic['user_submit'] = username
    try:
        print dic
        backend.add_application(dic)
        response = response_success()
    except ValidationError as e:
        response = response_from_validation_error(e)
    except Exception as e:
        print "Unexpected error: ", e
        response = response_from_exception(e)
    return JsonResponse(response)


def modify_application(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    dic['operator_admin'] = username
    backend.modify_application(dic)
    return HttpResponseRedirect('/admin')


def student_modify_application(request):
    try:
        dic = request.POST.dict()
        id = int(dic['application_id'])
        backend.del_application(id)
        submit_application(request)
        res = 'success'
    except (ValueError, AssertionError):
        res = 'failed'
    print res
    return HttpResponse(res)


def delete_application(request, id):
    backend.del_application(id)
    return HttpResponseRedirect('/admin')


def delete_official_account(request):
    print "delete_official_account", request.POST
    try:
        id = int(request.POST['id'])
        assert(backend.del_official_account(id))
        res = 'success'
    except (ValueError, AssertionError):
        res = 'failed'
    return HttpResponse(res)


def add_admin(request):
    dic = request.POST.dict()
    backend.add_admin(
        dic['username'],
        dic['password'],
        dic['email'],
        dic['description']
    )
    return HttpResponseRedirect('/superuser')


def del_admin(request):
    print "del %s" % request.POST['username']
    backend.del_admin(request.POST['username'])
    return HttpResponseRedirect('/superuser')


def add_message(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    backend.add_message(
        dic['category'],
        dic['official_account_id'],
        dic['title'],
        dic['content'],
        username
    )
    return HttpResponse(request.POST)


def process_message(request):
    account_id = request.POST['official_account_id']
    backend.process_all_messages(account_id)
    return HttpResponse(request.POST)


def submit_rule(request):
    dic = request.POST.dict()
    backend.add_forewarn_rule(dic)
    return HttpResponse(request.POST)
