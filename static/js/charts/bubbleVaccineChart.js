var bubbleOptions = {
    chart: {
        type: 'packedbubble',
        height: '100%'
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Vacunación'
    },
    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}</b>'
    },
    plotOptions: {
        packedbubble: {
            minSize: '0%',
            maxSize: '100%',
            zMin: 0,
            zMax: 100,
            layoutAlgorithm: {
                splitSeries: false,
                gravitationalConstant: 0.02
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}',
                style: {
                    color: 'black',
                    textOutline: 'none',
                    fontWeight: 'normal'
                }
            }
        }
    },
    series: [{
        name: 'Sin vacunar',
        color: '#0081c7',
        data: [{
            name: 'Sin vacunar',
            value: 80
        }]
    },
    {
        name: 'Una dosis',
        color: '#d9b500',
        data: [{
            name: "Una dosis",
            value: 10
        }]
    },
    {
        name: 'Dos dosis',
        color: '#c70700',
        data: [{
            name: "Dos dosis",
            value: 15
        }]
    }]
}

Highcharts.chart('bubbleVaccineChart', bubbleOptions);