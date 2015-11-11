from json import *


def encode_charts(xlist, ylist):
    data = []
    cnt = 0
    for it in xlist:
        data.append({
            'label': it,
            'value': ylist[cnt]
        })
        cnt += 1
    return JSONEncoder().encode(data)

    # print js_charts("column3d", "test", "subCaption", "xAxisName", "yAxisName", ["Jun", "July"], [1, 2])
