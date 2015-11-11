from json import *

pre_model = """
  FusionCharts.ready(function(){
    var revenueChart = new FusionCharts("""
out_model = """
    	);
revenueChart.render();
})
"""

def js_charts(chart_type, caption, subCaption, xAxisName, yAxisName, xlist, ylist):
	dic = {}
	dic['type'] = chart_type
	dic['renderAt'] = 'chartContainer'
	dic['width'] = 500
	dic['height'] = 300
	dic['dataFormat'] = 'json'
	dic['dataSource'] = {}
	dic['dataSource']['chart'] = {}
	chart = {"caption": caption,"subCaption": subCaption,"xAxisName": xAxisName,"yAxisName": yAxisName,"theme": "fint"}
	dic['dataSource']['chart'] = chart
	data = []
	cnt = 0
	for it in xlist:
		data.append({"label" : it, "value": ylist[cnt]})
		cnt = cnt + 1
	dic['dataSource']['data'] = data
	res = JSONEncoder().encode(dic)
	return pre_model + res + out_model

#print js_charts("column3d", "test", "subCaption", "xAxisName", "yAxisName", ["Jun", "July"], [1, 2])