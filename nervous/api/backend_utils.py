from api import getdata
import traceback


def verify_wx_name(wx_name):
    try:
        params = {'wx_name': wx_name}
        d = getdata.get_dict('wx/wxapi/nickname_one', params)
        return d['returnCode'] == '1001'
    except Exception as e:
        traceback.print_exc()
        return None
