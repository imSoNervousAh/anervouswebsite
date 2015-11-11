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
from django.conf.urls import url

urlpatterns = [
    # wechat part
    #   login/logout
    url(r'^index/?$', 'wechat.views.index', name='index'),
    url(r'^login/([^/]+)/?$', 'wechat.views.login', name='login'),
    url(r'^login', 'wechat.views.login', name='login'),
    url(r'^logout', 'wechat.views.logout', name='logout'),

    # change_info
    #    url(r'^change_info/?$','wechat.views.change_info',name='change_info'),

    #   message
    url(r'^message/[^/]+/?$', 'wechat.views.message_jump', name='message/jump'),
    url(r'^message/student/([0-9]+)/?$', 'wechat.views.message_detail_student', name='message/student'),
    url(r'^message/admin/([0-9]+)/?$', 'wechat.views.message_detail_admin', name='message/admin'),

    #   student
    url(r'^student/my_applications', 'wechat.views.student_show_applications', name='student/my-applications'),
    url(r'^student/add_application', 'wechat.views.student_add_applications', name='student/add-application'),
    url(r'^student/fill_info', 'wechat.views.student_fill_info', name='student/fill-info'),
    url(r'^student/change_info', 'wechat.views.student_change_info', name='student/change-info'),
    url(r'^student', 'wechat.views.student', name='student'),

    #   admin
    url(r'^admin/detail/([0-9]+)/articles_list/?$', 'wechat.views.admin_show_official_account_articles',
        name='admin/detail/articles-list'),
    url(r'^admin/detail/([0-9]+)/?$', 'wechat.views.admin_show_official_account_detail', name='admin/detail'),
    url(r'^admin/applications/(\w+)/?$', 'wechat.views.admin_show_applications', name='admin/applications'),
    url(r'^admin/official_accounts/?$', 'wechat.views.admin_show_official_accounts', name='admin/official-accounts'),
    url(r'^admin/articles/?$', 'wechat.views.admin_show_articles', name='admin/articles'),
    url(r'^admin/dashboard/?$', 'wechat.views.admin_dashboard', name='admin/dashboard'),
    url(r'^admin', 'wechat.views.admin', name='admin'),

    #   superuser
    url(r'^superuser/admin_list/?$', 'wechat.views.superuser_show_admins', name='superuser/admins'),
    url(r'^superuser', 'wechat.views.superuser', name='superuser'),

    # api part
    url(r'^api/login/([^/]+)/?$', 'api.views.login', name='api_login'),

    url(r'^api/submit_application/?$', 'api.views.submit_application', name='api/submit_application'),
    url(r'^api/submit_student_info/?$', 'api.views.submit_student_info', name='api/submit_student_info'),
    url(r'^api/modify_application/?$', 'api.views.modify_application', name='api/modify_application'),
    url(r'^api/add_admin/?$', 'api.views.add_admin', name='api/add_admin'),
    url(r'^api/del_admin/?$', 'api.views.del_admin', name='api/del_admin'),
    url(r'^api/add_message/?$', 'api.views.add_message', name='api/add_message'),
    url(r'^api/process_message/?$', 'api.views.process_message', name='api/process_message'),

    # not found part
    url(r'^notfound', 'wechat.views.notfound', name='notfound'),
    url(r'^$', 'wechat.views.index', name='index'),
    url(r'^[\s\S]*', 'wechat.views.to_notfound', name='to_notfound'),

]
