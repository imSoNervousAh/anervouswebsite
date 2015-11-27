import urllib2
import urllib
import codecs


def bind():
    # Make Http Head

    # use ddns to bind ip with domain, need to fill 'hostname' and 'myip'
    url = 'http://ddns.oray.com/ph/update?hostname=nervous.wicp.net&myip=166.111.206.69'

    User_Agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36'
    Cookie = 'connect.sid=s%3AuGZU_VeCrixsynOBkdFSyRbmGSNckCs5.%2F%2BvP0uWNiMTeKdpg22YvEvPc5vXY2o80yMkuLbU7gFQ'
    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    Renfer = 'http://ddns.oray.com/ph/update',
    Host = 'ddns.oray.com'
    Authorization = 'Basic eXRsMTM1MDgxMTExMDc6eXRsNTE4ODg4'

    headers = {
        'User-Agent': User_Agent,
        'Host': Host,
        'Accept': Accept,
        # 'Refer':Renfer,
        # 'Cookie': Cookie,
        'Authorization': Authorization,
    }

    # Make Http Body
    data = {
        # 'name': account
        'hostname': 'nervous.wcip.net',
        'myip': '166.111.206.69',
    }
    data = urllib.urlencode(data)

    # POST/GET
    try:
        req = urllib2.Request(url=url, headers=headers, data=data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        print the_page

        save = False
        if save == True:
            file = codecs.open('result.html', 'w')
            file.write(the_page)
    except urllib2.HTTPError as http_error:
        print http_error
        # print zlib.decompress(http_error.read(), 30)
