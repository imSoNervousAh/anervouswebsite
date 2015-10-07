import urllib
import urllib2
import copy
import hashlib
import base64
import json

basicURL = 'http://open.gsdata.cn/api/'
APP_ID = 'PycD3O1YpDHA1pU0yG7t'
APP_KEY = 'HLmQEmffw90JoN0wxYzd4QSaJ'

def jsonEncode(input) :
	resultString = '{'
	flag = 0
	for keys in input :
		if flag == 1 :
			resultString += ','
		resultString += '"'
		resultString += keys[0]
		resultString += '":"'
		resultString += keys[1]
		resultString += '"'
		flag = 1
	resultString += '}'
	return resultString

def encodeSignature(data) :
	ret = copy.deepcopy(data)
	sortedRet = sorted(ret.items(), key = lambda ret:ret[0])
	md5Res = hashlib.md5(jsonEncode(sortedRet).lower() + APP_KEY)
	res = md5Res.hexdigest()
	return res
def call(url, data) :
	dataCall = copy.deepcopy(data)
	dataCall['appid'] = APP_ID
	dataCall['signature'] = encodeSignature(dataCall)
	postString = jsonEncode(dataCall.items())
	tmpstring = base64.encodestring(postString)
	req = urllib2.Request(basicURL + url, tmpstring)
	response = urllib2.urlopen(req)
	the_page = response.read()
	return the_page
def getDict(url, paras):
	output = call(url, paras)
	d = json.loads(output)
	return d