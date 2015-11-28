# -*- coding=utf-8 -*-

from django import template

register = template.Library()


@register.filter(name='unprocessed_messages_count')
def unprocessed_messages_count(account, category):
    return account.unprocessed_messages_count(category)


@register.filter(name='wci')
def wci(account):
    if account.wci:
        return round(account.wci, 2)
    else:
        return u'尚未抓取'


@register.filter(name='views_total')
def views_total(account):
    if account.views_total:
        return account.views_total
    else:
        return u'尚未抓取'


@register.filter(name='likes_total')
def likes_total(account):
    if account.likes_total:
        return account.likes_total
    else:
        return u'尚未抓取'
