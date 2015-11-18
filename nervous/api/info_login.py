#!/usr/bin/env python
# coding:utf-8

import cookielib
import urllib
import urllib2

__username__ = 'username'
__password__ = 'password'


def auth_by_info(username, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    url_login = 'https://portal.tsinghua.edu.cn:443/Login'
    body = (
        ('userName', username),
        ('password', password),
        ('redirect', 'NO'),
    )

    try:
        text = opener.open(url_login, urllib.urlencode(body)).read().decode('utf-8')
    except:
        text = opener.open(url_login, urllib.urlencode(body)).read().decode('gb2312')
    
    seed = u'用户名或密码错误！'
    if text.find(seed) != -1:
        return False
    else:
        return True


if __name__ == '__main__':
    print auth_by_info(__username__, __password__)
