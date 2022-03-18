
//create a drawing context on the canvas
var $element = document.getElementById("pm");

if ($element !== null){
    var pm_analysisChart;
    var pm_analysis_ctx = $element.getContext("2d"),
        pm_data = {},
        pm_analysis_labels = ["fine","coarse"],
        pm_analysis_borderColor = {
            'fine': 'rgba(200, 0, 0, 1)',
            'coarse': 'rgba(0, 0, 200, 1)',
        },
        pm_analysis_backgroundColor = {
            'fine': 'rgba(200, 0, 0, .6)',
            'coarse': 'rgba(0, 0, 200, .6)',
        };

    // using jQuery ajax method get data from the external file. ( while using react you will do it differently)
    var jsonData = $.ajax({
        url: 'json/pm.json',
        dataType: 'json',
    }).done(function(results)
    {
        processedData = pm_analysisprocessData(results);

        var presets = window.chartColors;
        pm_data = {
            labels: processedData.x_labels,
            datasets: []
        };

        for(i=0; i<pm_analysis_labels.length; i++){
            pm_data['datasets'].push(
                {
                    label: pm_analysis_labels[i],
                    data: processedData.data[pm_analysis_labels[i]],
                    borderColor: processedData.borderColor[pm_analysis_labels[i]],
                    backgroundColor: processedData.backgroundColor[pm_analysis_labels[i]],
                    fill: true,
                }
            )

        }
        var options = {
            maintainAspectRatio: false,
            responsive: true,
            spanGaps: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Particulate matter for ' + results['datetime'].slice(0,10)
                },
            },
            scales: {
                x: {
                    display: true,
                    type: 'time',
                    time: {
                        parser: 'YYYY-MM-DD HH:mm',
                        tooltipFormat: 'HH:mm DD/MM/YYYY',
                        unit: 'hour',
                        unitStepSize: 10,
                        displayFormats: {
                            'day': 'DD/MM/YYYY',
                            'hour': 'DD-MM HH:mm',

                            'minute': 'DD/MM/YYYY HH:mm',
                        }
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'part/cm³'
                    }
                }
            },
        };

        pm_analysisChart = new Chart(pm_analysis_ctx, {
            type: 'line',
            data: pm_data,
            options: options
        });

    });

}

// translates the data json into an array that can be processed by Chart.js
var pm_analysisprocessData = function(jsonData)
{
    //var locale = "en-us";
    myformat = Intl.NumberFormat('it-it', { minimumIntegerDigits: 2 })
    var x_labels = Object.keys(jsonData["data"]).map(function(item) {
        return new Date(item);
    }).sort((a, b) => a - b);

    var dataSet = {},
        isodata = '';
    for(var i=0; i<pm_analysis_labels.length; i++){
        // a data set for each label
        dataSet[pm_analysis_labels[i]] = [];

        for (var j = 0; j < x_labels.length; j++) {
            // ci sono 3 ore di shift?
            date_string = x_labels[j].getFullYear()+'-'+myformat.format(x_labels[j].getMonth()+1)+'-'+myformat.format(x_labels[j].getDate())+' '+myformat.format(x_labels[j].getHours())+':'+myformat.format(x_labels[j].getMinutes())+':'+myformat.format(x_labels[j].getSeconds())

            if(jsonData["data"][date_string]){
                dataSet[pm_analysis_labels[i]].push(
                    jsonData["data"][date_string][pm_analysis_labels[i]])
            } else {
                console.log(date_string)
            }
        }
    }

    return {
        labels: pm_analysis_labels,
        x_labels: x_labels,
        data: dataSet,
        borderColor: pm_analysis_borderColor,
        backgroundColor: pm_analysis_backgroundColor
    }
};
