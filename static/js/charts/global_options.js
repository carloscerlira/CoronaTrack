var globalOptions = {
    credits: {
        enabled: false
    },
    xAxis: {
        type: 'datetime'
    },
    yAxis: {
        title: false,
        visible: false,
        endOnTick: false 
    },
    plotOptions: {
        series: {
            pointInterval: 24*3600*1000
        },
        line: {
            color: '#0056bf',
            lineWidth: 3
        },
        column: {
            crisp: false,
            borderWidth: 0,
            shadow: false
        }
    },
    series: []
}