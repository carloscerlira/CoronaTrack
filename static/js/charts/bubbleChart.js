var bubbleOptions = {
    chart: {
        type: 'packedbubble',
        height: '100%'
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Semáforo Epidemiológico'
    },
    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}</b>'
    },
    plotOptions: {
        packedbubble: {
            minSize: '30%',
            maxSize: '120%',
            zMin: 0,
            zMax: 1000,
            layoutAlgorithm: {
                splitSeries: true,
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
        name: 'Verde',
        color: '#12b82e',
        data: [{
            name: 'Ciudad de México',
            value: 1
        }, {
            name: 'Aguascalientes',
            value: 1
        },
        {
            name: "Baja California",
            value: 1
        },
        {
            name: "Campeche",
            value: 1
        },
        {
            name: "Coahuila",
            value: 1
        },
        {
            name: "Colima",
            value: 1
        },
        {
            name: "Chihuahua",
            value: 1
        },
        {
            name: "Chiapas",
            value: 1
        },
        {
            name: "Chihuahua",
            value: 1
        },
        {
            name: "Guanajuato",
            value: 1
        },
        {
            name: "Guerrero",
            value: 1
        },
        {
            name: "Jalisco",
            value: 1
        },
        {
            name: "México",
            value: 1
        },
        {
            name: "Morelos",
            value: 1
        },
        {
            name: "Nayarit",
            value: 1
        },
        {
            name: "Oaxaca",
            value: 1
        },
        {
            name: "Puebla",
            value: 1
        },
        {
            name: "Quéretaro",
            value: 1
        }]
    },
    {
        name: 'Amarillo',
        color: '#d9b500',
        data: [{
            name: "Sonora",
            value: 1
        },
        {
            name: "Sinaloa",
            value: 1
        },
        {
            name: "Nuevo León",
            value: 1
        },
        {
            name: "Tamaulipas",
            value: 1
        },
        {
            name: "Veracruz",
            value: 1
        },
        {
            name: "Colima",
            value: 1
        }]
    },
    {
        name: 'Naranja',
        color: '#d94500',
        data: [{
            name: "Quintana Roo",
            value: 1
        },
        {
            name: "Yucatán",
            value: 1
        },
        {
            name: "Tabasco",
            value: 1
        },
        {
            name: "Baja California Sur",
            value: 1
        }]
    }]
}

Highcharts.chart('bubbleChart', bubbleOptions);