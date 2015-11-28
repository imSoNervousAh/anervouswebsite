# -*-coding:utf-8

import traceback
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
# from api.info_login import auth_by_info as tsinghua_login
from api.usereg_login import check as tsinghua_login
from database import backend
from wechat import session
from multiprocessing import Process


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
    response = {
        'status': 'error',
        'error_messages': e.message_dict,
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
    """
        If a function ...
            throws an exception: return a JSON request indicating the error
            returns None: return a JSON request indicating success
            returns something other than None: decorated function will return that value

        This is intended to be the outer-most decorator of all view functions.
    """

    def wrapper(request, *args, **kwargs):
        ret = None
        try:
            ret = func(request, *args, **kwargs)
            response = response_success()
        except Exception as e:
            response = response_from_exception(e)
        print 'json_response_general_exception_decorator: ', ret, response
        return ret or JsonResponse(response)

    return wrapper


def json_response_validation_error_decorator(func):
    """
        If a function ...
            throws an ValidationError: return a JSON request indicating the error
            returns None: return a JSON request indicating success
            returns something other than None: return that value

        Also the function extract the 'method' value from request.POST to remind
        the front-end of the method through which the error was triggered.

        Generally we should decorate all view functions that create something in
        the database using this decorator.
    """

    def wrapper(request, *args, **kwargs):
        ret = None
        method = request.POST.dict().get('method', None)
        try:
            ret = func(request, *args, **kwargs)
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
    if settings.DEBUG and check_admin(username, password):
        return username.isdigit()
    else:
        return tsinghua_login(username, password)


def check_superuser(username, password):
    return (username == settings.SUPERUSER_USERNAME) and (password == settings.SUPERUSER_PASSWORD)


# Views

@json_response_general_exception_decorator
def login(request):
    username, password = request.POST['account'], request.POST['password']
    print username, password
    if settings.DEBUG:
        priority = ['superuser', 'student', 'admin']
    else:
        priority = ['superuser', 'admin', 'student']
    for identity in priority:
        print 'trying login with identity = %s' % identity
        if globals()['check_%s' % identity](username, password):
            session.add_session(request, identity=identity, username=username)
            return JsonResponse({
                'status': 'ok',
                'identity': identity,
            })
    session.del_session(request)
    return JsonResponse({
        'status': 'error',
        'error_message': u'用户名或密码错误！'
    })


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
@json_response_validation_error_decorator
def modify_application(request):
    dic = request.POST.dict()
    username = session.get_username(request)
    dic['operator_admin'] = username
    backend.modify_application(dic)


@json_response_general_exception_decorator
def delete_application(request, id):
    backend.del_application(id)


@json_response_general_exception_decorator
def recall_application(request, id):
    backend.recall_application(id)


@json_response_general_exception_decorator
def delete_official_account(request):
    id = int(request.POST['id'])
    backend.del_official_account(id)


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def add_admin(request):
    dic = request.POST.dict()
    backend.add_admin(
        dic['username'],
        dic['password'],
        dic['email'],
        dic['description']
    )


@json_response_general_exception_decorator
def del_admin(request):
    print "del %s" % request.POST['username']
    backend.del_admin(request.POST['username'])


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
    category = request.POST['category']
    backend.process_all_messages(account_id, category)


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def submit_rule(request):
    dic = request.POST.dict()
    backend.add_forewarn_rule(dic)


@json_response_general_exception_decorator
@json_response_validation_error_decorator
def modify_rule(request):
    dic = request.POST.dict()
    print dic
    backend.modify_forewarn_rule(dic)


@json_response_general_exception_decorator
def delete_forewarn_rule(request, id):
    backend.del_forewarn_rule(id)


@json_response_general_exception_decorator
def update_start(request):
    def worker():
        try:
            backend.update_all()
        except Exception as e:
            traceback.print_exc()

    p = Process(target=worker)
    p.start()


@json_response_general_exception_decorator
def modify_announcement(request):
    announcement = request.POST['content']
    backend.modify_announcement(announcement)
