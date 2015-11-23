import base64
import copy
import hashlib
import json
import urllib2

basicURL = 'http://open.gsdata.cn/api/'
APP_ID = 'PycD3O1YpDHA1pU0yG7t'
APP_KEY = 'HLmQEmffw90JoN0wxYzd4QSaJ'


def json_encode(input):
    result_string = '{'
    flag = 0
    for keys in input:
        if flag == 1:
            result_string += ','
        result_string += '"'
        result_string += keys[0]
        result_string += '":"'
        result_string += str(keys[1])
        result_string += '"'
        flag = 1
    result_string += '}'
    return result_string


def encode_signature(data):
    ret = copy.deepcopy(data)
    sorted_ret = sorted(ret.items(), key=lambda ret: ret[0])
    md5_res = hashlib.md5(json_encode(sorted_ret).lower() + APP_KEY)
    res = md5_res.hexdigest()
    return res


def call(url, data):
    data_call = copy.deepcopy(data)
    data_call['appid'] = APP_ID
    data_call['signature'] = encode_signature(data_call)
    post_string = json_encode(data_call.items())
    tmp_string = base64.encodestring(post_string)
    req = urllib2.Request(basicURL + url, tmp_string)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def get_dict(url, paras):
    output = call(url, paras)
    d = json.loads(output)
    return d
