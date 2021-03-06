var dailyRecovered = {
    chart: {
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Daily new dosis'
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
            pointStart: time_series['starts']['vaccines'],
            pointInterval: 24*3600*1000
        },
        line: {
            color: '#0056bf',
        },
        column: {
            shadow: false,
            pointPadding: 0,
            borderWidth: 0,
            crisp: false,
        },
        area: {
            color: '#0056bf',
            fillOpacity: 0.15
        }
    },
    series: [
        {
            name: 'Daily new dosis given',
            type:'column',
            data: time_series['daily_vaccines']
        },
        {
            name: '7MA',
            type:'area',
            data: time_series['7MA_daily_vaccines']
        }
    ]
}
Highcharts.chart('dailyVaccineChart', dailyRecovered);
