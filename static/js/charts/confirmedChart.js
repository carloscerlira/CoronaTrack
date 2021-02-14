var confirmedOptions = {
    chart: {
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Total cases'
    },
    subtitle: {
        text: general['country']
    },
    xAxis: {
        type: 'datetime'
    },
    yAxis: {
        title: false,
        visible: false,
        endOnTick: false,
        min:0
    },
    tooltip: {
        valueDecimals: 0
    },
    plotOptions: {
        series: {
            pointStart: time_series['starts']['confirmed'],
            pointInterval: 24*3600*1000
        },
        line: {
            color: '#0056bf',
        },
        column: {
            pointWidth: 1,
            shadow: false,
            pointPadding: 0,
            borderWidth: 0,
            crisp: false,
        },
        area: {
            color: '#0056bf',
            fillOpacity: 0.2
        }
    },
    series: [
        {
            name: 'Total cases',
            type:'area',
            data: time_series['confirmed']
        }
    ]
}
Highcharts.chart('confirmedChart', confirmedOptions);
