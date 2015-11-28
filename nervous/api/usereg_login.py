import hashlib
import urllib2

def md5_hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def check(username, password):
    data = 'action=login&user_login_name=%s&user_password=%s' % (
        username,
        # md5_hash(password),
        password, # front-end already md5-ed it
    )
    url = 'http://usereg.tsinghua.edu.cn/do.php'
    response = urllib2.urlopen(url, data)
    return response.read() == 'ok'
