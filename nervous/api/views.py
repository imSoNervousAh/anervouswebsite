# -*-coding:utf-8

from database import backend
from wechat import session
from api.info_login import auth_by_info as tsinghua_login
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
import traceback


# Utils

def response_success(method=None):
    response = {
        'status': 'ok',
    }
    if method:
        response['submit_method'] = method
    return response


def response_from_validation_error(e, method=None):
    if settings.DEBUG:
        print '=============================='
        traceback.print_exc()
        print '=============================='
    error_dict = e.message_dict
    key, value = error_dict.popitem()
    response = {
        'status': 'error',
        'error_message': value,
        'error_field': key,
    }
    if method:
        response['submit_method'] = method
    return response


def response_from_exception(e):
    print '=============================='
    traceback.print_exc()
    print '=============================='
    response = {
        'status': 'error',
        'error_message': e.__unicode__(),
    }
    return response


def json_response_general_exception_decorator(func):
    def wrapper(request):
        ret = None
        try:
            ret = func(request)
            response = response_success()
        except Exception as e:
            response = response_from_exception(e)
        print 'json_response_general_exception_decorator: ', ret, response
        return ret or JsonResponse(response)
    return wrapper


def json_response_validation_error_decorator(func):
    def wrapper(request):
        ret = None
        method = request.POST.dict().get('method', None)
        try:
            ret = func(request)
            response = response_success(method)
        except ValidationError as e:
            response = response_from_validation_error(e, method)
        print 'json_response_wrapper_with_submit_method: ', method, response
        return ret or JsonResponse(response)
    return wrapper


def json_response_decorator(func):
    return json_response_general_exception_decorator(func)


# Helper functions

def check_admin(username, password):
    return backend.check_admin(username, password)


def check_student(username, password):
    if settings.DEBUG:
        fake_student = check_admin(username, password)
    else:
        fake_student = False
    return fake_student or tsinghua_login(username, password)


def check_superuser(username, password):
    return (username == 'root') and (password == 'e10adc3949ba59abbe56e057f20f883e')  # hex_md5('123456')


# Views

def login(request, identity):
    username, password = request.POST['account'], request.POST['password']
    print '[', identity, '] is trying to login...'
    print '[account] ', username
    print '[password] ', password
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


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def submit_student_info(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    backend.set_student_information(username, dic)


@json_response_general_exception_decorator
def get_application_status_from_method(method):
    status = {
        'submit': 'pending',
        'save': 'not_submitted',
    }
    return status[method]


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def submit_application(request):
    dic = request.POST.dict()
    method = dic['method']
    username = session.get_username(request)
    dic['user_submit'] = username
    dic['status'] = get_application_status_from_method(method)
    backend.add_application(dic)


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def student_modify_application(request):
    dic = request.POST.dict()
    method = dic['method']
    username = session.get_username(request)
    dic['user_submit'] = username
    dic['status'] = get_application_status_from_method(method)
    backend.student_modify_application(dic)


@json_response_general_exception_decorator
def modify_application(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    dic['operator_admin'] = username
    backend.modify_application(dic)
    return HttpResponseRedirect('/admin')


# @json_response_general_exception_decorator
def delete_application(request, id):
    backend.del_application(id)
    return HttpResponse(request)

# @json_response_general_exception_decorator
def recall_application(request, id):
    print 'recall'
    return HttpResponse(request)


@json_response_general_exception_decorator
def delete_official_account(request):
    id = int(request.POST['id'])
    backend.del_official_account(id)


@json_response_general_exception_decorator
def add_admin(request):
    dic = request.POST.dict()
    print 'add admin...'
    print '[account] ',dic['username']
    print '[password]',dic['password']
    backend.add_admin(
        dic['username'],
        dic['password'],
        dic['email'],
        dic['description']
    )
    return HttpResponseRedirect('/superuser')


@json_response_general_exception_decorator
def del_admin(request):
    print "del %s" % request.POST['username']
    backend.del_admin(request.POST['username'])
    return HttpResponseRedirect('/superuser')


@json_response_general_exception_decorator
@json_response_decorator
def add_message(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    backend.add_message(
        dic['category'],
        dic['official_account_id'],
        dic['content'],
        username
    )


@json_response_general_exception_decorator
def process_message(request):
    account_id = request.POST['official_account_id']
    backend.process_all_messages(account_id)
    # return HttpResponse(request.POST)


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def submit_rule(request):
    dic = request.POST.dict()
    backend.add_forewarn_rule(dic)
