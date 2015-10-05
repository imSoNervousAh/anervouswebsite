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
    #wechat part
	url(r'^login','wechat.views.login',name='login'),
    url(r'^student','wechat.views.student',name='student'),
    url(r'^manager','wechat.views.manager',name='manager'),
    url(r'^supermanager','wechat.views.supermanager',name='supermanager'),
    url(r'^admin/', include(admin.site.urls)),
    
    #api part
    url(r'^api/login','api.views.login',name='login'),

    #not found part
    url(r'^notfound','wechat.views.notfound',name='notfound'),
    url(r'^$','wechat.views.index',name='index'),
    url(r'^[\s\S]*','wechat.views.to_notfound',name='to_notfound'),


]
