var dailyDeathsOptions = {
    chart: {
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Daily new deaths'
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
        min: 0
    },
    tooltip: {
        valueDecimals: 0
    },
    plotOptions: {
        series: {
            pointStart: general['start'],
            pointInterval: 24*3600*1000
        },
        line: {
            color: '#0056bf',
        },
        column: {
            shadow: false,
            borderWidth: 0,
            groupPadding: 0.3,
            crisp: false,
        },
        area: {
            color: '#0056bf',
            fillOpacity: 0.15,
        }
    },
    series: [
        {
            name: 'Daily new deaths',
            type:'column',
            data: time_series['daily_deaths']
        },
        {
            name: '7MA',
            type:'area',
            data: time_series['7MA_daily_deaths']
        }
    ]
}
Highcharts.chart('dailyDeathsChart', dailyDeathsOptions);