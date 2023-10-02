var csvFilePath = 'data/umap_visualization.csv';
var traces;

function closeInfoBox() {
    infoBox.style.display = 'none';
}

function searchName() {
    var searchInput = document.getElementById("nameSearchInput").value;
    if (searchInput.length < 3) {
        alert("Please enter at least 3 letters to search.");
        return;
    }

    var selectedDataPoints = [];
    var customDataArray = [];
    var tracesOfSelectedPoints = [];

    var layout = {
        xaxis: {
            title: '',
            showgrid: true,
            zeroline: false,
            showticklabels: false,
        },
        yaxis: {
            title: '',
            showgrid: true,
            zeroline: false,
            showticklabels: false,
        },
        hoverlabel: {
            font: {
                size: 20,
            },
        },
        legend: {
            font: {
                size: 20,
            },
        },
        modebar: {
            orientation: 'h',
            bgcolor: 'black',
            color: '#d0000b',
            activecolor: '#fde242',
            x: 0,
            y: 0
        },
        hovermode: 'closest',
        showlegend: false,
        scrollZoom: true,
        plot_bgcolor: '#FDF7F0'
    };

    for (var i = 0; i < traces.length; i++) {
        var trace = traces[i];
        var selectedTrace = {
            x: [],
            y: [],
            mode: 'markers',
            type: 'scatter',
            customdata: [],
            hovertemplate: '<b>Name</b>: %{customdata.name}<br><b>Citation</b>: %{customdata.citation}<br><b>Cluster</b>: ' + (i + 1) + '<br><b>Keywords</b>: %{customdata.keywords}',
            name: trace.name,
            marker: {
                size: 25,
                colorscale: 'Jet',
            },
        };

        customDataArray = trace.customdata;

        for (var j = 0; j < customDataArray.length; j++) {
            var name = customDataArray[j].name.toLowerCase();

            if (name.includes(searchInput.toLowerCase())) {
                var customDataArrayy = {
                    name: customDataArray[j].name,
                    citation: customDataArray[j].citation,
                    keywords: trace.text[j]
                };

                selectedDataPoints.push(j);
                selectedTrace.x.push(trace.x[j]);
                selectedTrace.y.push(trace.y[j]);
                selectedTrace.customdata.push(customDataArrayy);

                tracesOfSelectedPoints.push(selectedTrace);
            }
        }
    }

    Plotly.newPlot(
        'scatter-plot',
        tracesOfSelectedPoints,
        layout,
        {
            responsive: true
        }
    );

    // var modeBar = document.querySelector('.modebar-container');
    // modeBar.style.position = 'absolute';
    // modeBar.style.left = '-860px';
    // modeBar.style.top = '10px';

    var plotContainer2 = document.getElementById('scatter-plot');
    plotContainer2.on('plotly_click', function (eventData) {
        var regex = /\d+/;

        var selectedData = eventData.points[0].customdata;
        var clusterName = eventData.points[0].data.name;

        document.getElementById('name').textContent = selectedData.name;
        document.getElementById('citation').textContent = selectedData.citation;
        document.getElementById('cluster').textContent = clusterName.match(regex);
        document.getElementById('keywords').textContent = selectedData.keywords;

        infoBox.style.display = 'block';
    });

}

function resetChart() {
    plot();
}

document.getElementById('resetButton').addEventListener('click', resetChart);

function plot() {
    fetch(csvFilePath)
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(function (csvData) {
            Papa.parse(csvData, {
                header: true,
                dynamicTyping: true,
                complete: function (results) {

                    var parsedData = results.data;
                    traces = [];

                    for (var i = 1; i <= 10; i++) {
                        var filteredData = parsedData.filter(function (row) {
                            return row.cluster === i - 1;
                        });

                        var xData = filteredData.map(function (row) {
                            return row.x;
                        });
                        var yData = filteredData.map(function (row) {
                            return row.y;
                        });
                        var keywordsData = filteredData.map(function (row) {
                            return row.keywords;
                        });

                        var customDataArray = filteredData.map(function (row) {
                            return {
                                name: row["Full Name"],
                                citation: row["Citation"]
                            };
                        });

                        var trace = {
                            x: xData,
                            y: yData,
                            mode: 'markers',
                            text: keywordsData,
                            customdata: customDataArray,
                            hovertemplate: '<b>Name</b>: %{customdata.name}<br><b>Citation</b>: %{customdata.citation}<br><b>Cluster</b>: ' + i + '<br><b>Keywords</b>: %{text}',
                            marker: {
                                size: 10,
                                colorscale: 'Jet',
                            },
                            type: 'scatter',
                            name: 'Cluster ' + i
                        };
                        traces.push(trace);
                    }

                    var layout = {
                        xaxis: {
                            title: '',
                            showgrid: true,
                            zeroline: false,
                            showticklabels: false,
                        },
                        yaxis: {
                            title: '',
                            showgrid: true,
                            zeroline: false,
                            showticklabels: false,
                        },
                        hoverlabel: {
                            font: {
                                size: 15,
                            },
                        },
                        legend: {
                            font: {
                                size: 20,
                            },
                        },
                        modebar: {
                            orientation: 'h',
                            bgcolor: 'black',
                            color: '#d0000b',
                            activecolor: '#fde242',
                            x: 0,
                            y: 0
                        },
                        hovermode: 'closest',
                        showlegend: true,
                        scrollZoom: true,
                        plot_bgcolor: '#FDF7F0'
                    };

                    Plotly.newPlot(
                        'scatter-plot',
                        traces,
                        layout,
                        {
                            scrollZoom: true,
                            modeBarButtonsToRemove: ['autoScale2d'],
                            displaylogo: false,
                            displayModeBar: true,
                            responsive: true
                        }
                    );

                    // var modeBar = document.querySelector('.modebar-container');
                    // modeBar.style.position = 'absolute';
                    // modeBar.style.left = '-860px';
                    // modeBar.style.top = '10px';

                    var plotContainer = document.getElementById('scatter-plot');

                    traces.forEach(function (trace, i) {

                        trace.customdata.forEach(function (dataObj) {
                            dataObj.traceNumber = i;
                        });
                    });

                    var infoBox = document.getElementById('infoBox');

                    plotContainer.on('plotly_click', function (eventData) {
                        var pointIndex = eventData.points[0].pointIndex;
                        var selectedData = eventData.points[0].customdata;
                        var traceNumber = selectedData.traceNumber;

                        document.getElementById('name').textContent = selectedData.name;
                        document.getElementById('citation').textContent = selectedData.citation;
                        document.getElementById('cluster').textContent = '' + (traceNumber + 1);
                        document.getElementById('keywords').textContent = traces[traceNumber].text[pointIndex];

                        infoBox.style.display = 'block';
                    });

                    plotContainer.on('plotly_relayout', function (eventData) {
                        var zoomFactor = eventData['xaxis.range[1]'] - eventData['xaxis.range[0]'];
                        if (isNaN(zoomFactor)) {
                            newMarkerSize = 10
                        } else if (zoomFactor < 6) {
                            var newMarkerSize = 50 / zoomFactor;
                        }

                        Plotly.update('scatter-plot', {
                            'marker.size': newMarkerSize
                        });
                    });
                },
                error: function (error) {
                    console.error('Error parsing CSV:', error);
                }
            });
        })
        .catch(function (error) {
            console.error('There was a problem with the fetch operation:', error);
        });

}

plot()