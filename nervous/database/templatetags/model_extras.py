# -*- coding=utf-8 -*-

from django import template

register = template.Library()


@register.filter(name='unprocessed_messages_count')
def unprocessed_messages_count(account, category):
    return account.unprocessed_messages_count(category)


@register.filter(name='wci')
def wci(account):
    if account.wci:
        return account.wci
    else:
        return u'尚未抓取'
