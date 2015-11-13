function renderChart(container, data_json, params, callback) {
    FusionCharts.ready(function () {
        var chart_data = {
            chart: {
                caption: "Caption",
                subCaption: "Top 5 stores in last month by revenue",
                theme: "zune",
                exportEnabled: "1",
                xAxisName: "",
                yAxisName: ""
            },
            data: data_json
        };
        $.extend(chart_data.chart, params);
        var chart_params = {
            type: 'doughnut2d',
            dataFormat: 'json',
            dataSource: chart_data
        };
        $.extend(chart_params, params);
        var myChart = new FusionCharts(chart_params);

        // Render the chart.
        if (container.substr(0, 1) == '#')
            container = container.substr(1);
        myChart.render(container, 'replace', function () {
            $("rect[fill=\"url('#11-90-rgba_204_204_204_1__0-rgba_255_255_255_1__100')\"]").remove();
            if (typeof callback === "function")
                callback(container);
        });
    });
}

function renderMultiChart(container, data, params, callback) {
    FusionCharts.ready(function () {
        var chart_data = data;
        var chart_params = {
            type: 'mscombidy2d',
            dataFormat: 'json',
            dataSource: chart_data
        };
        $.extend(chart_params, params);
        var myChart = new FusionCharts(chart_params);

        // Render the chart.
        if (container.substr(0, 1) == '#')
            container = container.substr(1);
        myChart.render(container, 'replace', function () {
            $("rect[fill=\"url('#11-90-rgba_204_204_204_1__0-rgba_255_255_255_1__100')\"]").remove();
            if (typeof callback === "function")
                callback(container);
        });
    });
}
