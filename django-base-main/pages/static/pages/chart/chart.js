export function initialize() {
    /*
    * Chart
    */
    const renderChart = async (response) => {
        // Show a quick 'no data' view if data not populated from Wikipedia
        if (response.series.length === 0) {
            document.getElementById('chart-container').prepend("No chart data - click the button above to fetch data from Wikipedia's API");
            return;
        }

        const container = echarts.init(document.getElementById('chart-container'));

        window.onresize = function() {
            container.resize();
        };
        
        // The vertical dashed lines overlaying the solar event data on the chart
        let markLineData = [];
        for (let idx in response.markLineData) {
            markLineData.push({
                y: '86%',
                xAxis: response.markLineData[idx].date,
                label: {
                    show: true
                },
                eventName: response.markLineData[idx].name
            })
        }

        const markLine = {
            symbol: 'none',
            tooltip: {
                formatter: (params) => {
                    return params.data.eventName;
                }
            },
            data: markLineData
        }

        response.series[0].markLine = markLine;

        // The chart config itself
        var cfg = {
            title: {
                text: 'Article revisions and solar industry events'
            },
            tooltip: {},
            dataZoom: [{
                type: 'slider'
            }, {
                type: 'inside'
            }],
            animation: false,
            xAxis: {
                data: response.xAxis
            },
            yAxis: {
            },
            series: response.series,
        };

        container.setOption(cfg);
    }

    /*
    * Data
    */
    const getData = async (url) => {
        const response = await fetch(url, {
            method: "GET"
        });

        return await response.json();
    }

    // Make async call to backend to populate chart data, then load ECharts using it
    getData('/pages/chart_data')
        .then(renderChart);
}

