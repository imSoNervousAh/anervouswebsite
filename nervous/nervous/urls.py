"""nervous URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # wechat part
    url(r'^index/?$', 'wechat.views.index', name='index'),
    url(r'^login/([^/]+)/?$', 'wechat.views.login', name='login'),
    url(r'^login', 'wechat.views.login'),
    url(r'^student', 'wechat.views.student', name='student'),
    url(r'^administrator/detail/(\d+)$', 'wechat.views.detail', name='detail'),
    url(r'^administrator', 'wechat.views.administrator', name='administrator'),
    url(r'^superuser', 'wechat.views.superuser', name='superuser'),
    url(r'^admin/', include(admin.site.urls)),
    
    # api part
    url(r'^api/login/([^/]+)/?$', 'api.views.login', name='api_login'),
    url(r'^api/submit_application', 'api.views.submit_application', name='submit_application'),
    url(r'^api/modify_application', 'api.views.modify_application', name='modify_application'),
    url(r'^api/add_admin', 'api.views.add_admin', name='add_admin'),
    url(r'^api/del_admin', 'api.views.del_admin', name='del_admin'),

    # not found part
    url(r'^notfound', 'wechat.views.notfound', name='notfound'),
    url(r'^$', 'wechat.views.index', name='index'),
    url(r'^[\s\S]*', 'wechat.views.to_notfound', name='to_notfound'),

]
