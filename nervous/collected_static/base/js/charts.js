function renderChart(container, type, data, params, callback) {
    FusionCharts.ready(function () {
        data['chart']['baseFont'] = $("body").css("font-family");
        data['chart']['theme'] = 'zune';
        data['chart']['exportEnabled'] = '1';
        var chart_params = {
            type: type,
            dataFormat: 'json',
            dataSource: data
        };
        $.extend(chart_params, params);
        var myChart = new FusionCharts(chart_params);

        // Render the chart.
        if (container.substr(0, 1) == '#')
            container = container.substr(1);
        myChart.render(container, 'replace', function () {
//            $("rect[fill=\"url('#11-90-rgba_204_204_204_1__0-rgba_255_255_255_1__100')\"]").remove();
//            $("rect[fill=\"url('#136-90-rgba_204_204_204_1__0-rgba_255_255_255_1__100')\"]").remove();
            $("rect[style=\"stroke: rgb(187, 187, 187); opacity: 1; fill-opacity: 1; stroke-opacity: 1;\"]").remove();

            if (typeof callback === "function")
                callback(container);
        });
    });
}
