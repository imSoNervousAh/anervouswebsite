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
from wechat import views
from api import views as apiviews

urlpatterns = [
    # wechat part
    #   login/logout
    url(r'^index/?$', views.index, name='index'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),

    #   home
    url(r'^home/?$', views.home, name='home'),

    #   message
    url(r'^message/[^/]+/?$', views.message_jump, name='message/jump'),
    url(r'^message/student/([0-9]+)/?$', views.message_detail_student, name='message/student'),
    url(r'^message/admin/([0-9]+)/?$', views.message_detail_admin, name='message/admin'),

    #   student
    url(r'^student/my_applications', views.student_show_applications, name='student/my-applications'),
    url(r'^student/add_application', views.student_add_applications, name='student/add-application'),
    url(r'^student/modify_application/([0-9]+)/?$', views.student_modify_applications,
        name='student/modify-application'),
    url(r'^student/fill_info', views.student_fill_info, name='student/fill-info'),
    url(r'^student/change_info', views.student_change_info, name='student/change-info'),
    url(r'^student', views.student, name='student'),

    #   admin
    url(r'^admin/detail/([0-9]+)/articles/list/?$', views.admin_show_official_account_articles_list,
        name='admin/detail/articles-list'),
    url(r'^admin/detail/([0-9]+)/statistics/?$', views.admin_show_official_account_statistics,
        name='admin/detail/statistics'),
    url(r'^admin/detail/([0-9]+)/articles/?$', views.admin_show_official_account_articles,
        name='admin/detail/articles'),
    url(r'^admin/detail/([0-9]+)/?$', views.admin_show_official_account_detail, name='admin/detail'),

    url(r'^admin/applications/(\w+)/?$', views.admin_show_applications, name='admin/applications'),
    url(r'^admin/applications/(\w+)/list/?$', views.admin_show_applications_list,
        name='admin/applications-list'),

    url(r'^admin/official_accounts/?$', views.admin_show_official_accounts, name='admin/official-accounts'),
    url(r'^admin/official_accounts/list/(\w+)/?$', views.admin_show_official_accounts_list,
        name='admin/official-accounts-list'),

    url(r'^admin/statistics/?$', views.admin_show_statistics, name='admin/statistics'),

    url(r'^admin/articles/?$', views.admin_show_articles, name='admin/articles'),
    url(r'^admin/articles/list/?$', views.admin_show_articles_list, name='admin/articles-list'),

    url(r'^admin/dashboard/?$', views.admin_dashboard, name='admin/dashboard'),

    url(r'^admin/forewarn_rules/?$', views.admin_forewarn_rules, name='admin/forewarn-rules'),
    url(r'^admin/forewarn_rules/list/?$', views.admin_forewarn_rules_list, name='admin/forewarn-rules-list'),
    url(r'^admin/forewarn_records/?$', views.admin_forewarn_records, name='admin/forewarn-records'),
    url(r'^admin/forewarn_records/list/?$', views.admin_forewarn_records_list,
        name='admin/forewarn-records-list'),

    url(r'^admin', views.admin, name='admin'),

    #   superuser
    url(r'^superuser/admin_list/?$', views.superuser_show_admins, name='superuser/admins'),
    url(r'^superuser/modify_announcement/?$', views.superuser_modify_announcement,
        name='superuser/modify-announcement'),
    url(r'^superuser/manage_database/?$', views.superuser_manage_database, name='superuser/manage-database'),
    url(r'^superuser/update_database/?$', views.superuser_update_database, name='superuser/update-database'),
    url(r'^superuser/progress_item/?$', views.superuser_progress_item, name='superuser/progress-item'),
    url(r'^superuser', views.superuser, name='superuser'),

    #   modals
    url(r'^modals/superuser/add_admin_modal/?$', views.superuser_show_add_admin_modal,
        name='modals/superuser/add-admin-modal'),
    url(r'^modals/admin/application_modal/process/(?P<id>\d+)/?$', views.admin_show_application_modal,
        {'type': 'process'}, name='modals/admin/process-application-modal'),
    url(r'^modals/admin/application_modal/view/(?P<id>\d+)/?$', views.admin_show_application_modal,
        {'type': 'view'}, name='modals/admin/view-application-modal'),
    url(r'^modals/admin/forewarn_rules_modal/modify/(?P<id>\d+)/?$', views.admin_show_forewarn_rules_modal,
        {'type': 'modify'}, name='modals/admin/modify-forewarn-rules-modal'),
    url(r'^modals/admin/forewarn_rules_modal/add/?$', views.admin_show_forewarn_rules_modal,
        {'type': 'add'}, name='modals/admin/add-forewarn-rules-modal'),

    #   badges
    url(r'^badges/student/pending_count/?$', views.student_badge_pending_count,
        name='badges/student/pending-count'),
    url(r'^badges/admin/pending_count/?$', views.admin_badge_pending_count, name='badges/admin/pending-count'),
    url(r'^badges/student/account-unprocessed-message-count/(\d+)/?$',
        views.student_badge_account_unprocessed_message_count,
        name='badges/student/account-unprocessed-message-count'),

    # api part
   url(r'^api/login/?$', apiviews.login, name='api/login'),

    url(r'^api/submit_application/?$', apiviews.submit_application, name='api/submit_application'),
    url(r'^api/modify_application/?$', apiviews.modify_application, name='api/modify_application'),
    url(r'^api/delete_application/([0-9]+)/?$', apiviews.delete_application, name='api/delete_application'),
    url(r'^api/recall_application/([0-9]+)/?$', apiviews.recall_application, name='api/recall_application'),
    url(r'^api/submit_student_info/?$', apiviews.submit_student_info, name='api/submit_student_info'),
    url(r'^api/student_modify_application/?$', apiviews.student_modify_application,
        name='api/student_modify_application'),
    url(r'^api/delete_official_account/?$', apiviews.delete_official_account, name='api/delete_official_account'),
    url(r'^api/add_admin/?$', apiviews.add_admin, name='api/add_admin'),
    url(r'^api/del_admin/?$', apiviews.del_admin, name='api/del_admin'),
    url(r'^api/add_message/?$', apiviews.add_message, name='api/add_message'),
    url(r'^api/process_message/?$', apiviews.process_message, name='api/process_message'),
    url(r'^api/submit_rule/?$', apiviews.submit_rule, name='api/submit_rule'),
    url(r'^api/modify_rule/?$', apiviews.modify_rule, name='api/modify_rule'),
    url(r'^api/update_start/?$', apiviews.update_start, name='api/update-start'),
    url(r'^api/modify_announcement/?$', apiviews.modify_announcement, name='api/modify_announcement'),
    url(r'^api/delete_forewarn_rule/([0-9]+)/?$', apiviews.delete_forewarn_rule, name='api/delete_forewarn_rule'),
    # not found part
    url(r'^notfound', views.notfound, name='notfound'),
    url(r'^$', views.index, name='index'),
    url(r'^[\s\S]*', views.to_notfound, name='to_notfound'),

]
