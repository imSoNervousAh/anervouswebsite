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
    #  login/logout
    url(r'^index/?$', 'wechat.views.index', name='index'),
    url(r'^login/([^/]+)/?$', 'wechat.views.login', name='login'),
    url(r'^login', 'wechat.views.login',name='login'),
    url(r'^logout','wechat.views.logout',name='logout'),

    #  student
    url(r'^student/my-applications/$', 'wechat.views.student_show_applications', name='student/my-applications'),
    url(r'^student/add-application/$', 'wechat.views.student_add_applications', name='student/add-application'),
    url(r'^student', 'wechat.views.student', name='student'),

    #  administrator
    url(r'^administrator/message/([0-9]+)/?', 'wechat.views.message', name='admin/message'),
    url(r'^administrator/detail/([0-9]+)/$', 'wechat.views.admin_show_official_account_detail', name='admin/detail'),
    url(r'^administrator/applications/(\w+)/$', 'wechat.views.admin_show_applications', name='admin/applications'),
    url(r'^administrator/official_accounts/$', 'wechat.views.admin_show_official_accounts', name='admin/official-accounts'),
    url(r'^administrator/articles/$', 'wechat.views.admin_show_articles', name='admin/articles'),
    url(r'^administrator/dashboard/$', 'wechat.views.admin_dashboard', name='admin/dashboard'),
    url(r'^administrator/message/([0-9]+)/$', 'wechat.views.message', name='message'),
    url(r'^administrator', 'wechat.views.admin', name='administrator'),

    #  superuser
    url(r'^superuser/admin_list/$', 'wechat.views.superuser_show_admins', name='superuser/admins'),
    url(r'^superuser', 'wechat.views.superuser', name='superuser'),

    # django admin
    url(r'^admin/', include(admin.site.urls)),
    
    # api part
    url(r'^api/login/([^/]+)/?$', 'api.views.login', name='api_login'),

    url(r'^api/submit_application', 'api.views.submit_application', name='api/submit_application'),
    url(r'^api/modify_application', 'api.views.modify_application', name='api/modify_application'),
    url(r'^api/add_admin', 'api.views.add_admin', name='api/add_admin'),
    url(r'^api/del_admin', 'api.views.del_admin', name='api/del_admin'),
    url(r'^api/add_message', 'api.views.add_message', name='add_message'),

    # not found part
    url(r'^notfound', 'wechat.views.notfound', name='notfound'),
    url(r'^$', 'wechat.views.index', name='index'),
    url(r'^[\s\S]*', 'wechat.views.to_notfound', name='to_notfound'),

]
