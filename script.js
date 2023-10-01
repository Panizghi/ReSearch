var csvFilePath = 'data/umap_visualization.csv';

function closeInfoBox() {
    infoBox.style.display = 'none';
}

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
                var traces = [];

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
                            authorName: row["Full Name"],
                            citation: row["Citation"]
                        };
                    });

                    var trace = {
                        x: xData,
                        y: yData,
                        mode: 'markers',
                        text: keywordsData,
                        customdata: customDataArray,
                        hovertemplate: 'Author Name: %{customdata.authorName}<br>Citation: %{customdata.citation}<br>Cluster: ' + i + '<br>Keywords: %{text}',
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
                        displayModeBar: true
                    }
                );

                var modeBar = document.querySelector('.modebar-container');
                modeBar.style.position = 'absolute';
                modeBar.style.left = '-860px';
                modeBar.style.top = '10px';

                var plotContainer = document.getElementById('scatter-plot');
                var clusterData = [];

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

                    document.getElementById('authorName').textContent = selectedData.authorName;
                    document.getElementById('citation').textContent = selectedData.citation;
                    document.getElementById('cluster').textContent = '' + (traceNumber + 1);
                    document.getElementById('keywords').textContent = traces[traceNumber].text[pointIndex];

                    infoBox.style.display = 'block';
                });


                var plotContainer = document.getElementById('scatter-plot');
                plotContainer.on('plotly_relayout', function (eventData) {
                    var zoomFactor = eventData['xaxis.range[1]'] - eventData['xaxis.range[0]'];
                    console.log(zoomFactor)
                    console.log('sdfsadffsadfsadadsfsadf')
                    if (isNaN(zoomFactor)) {
                        newMarkerSize = 10
                    } else if (zoomFactor < 6) {
                        var newMarkerSize = 50 / zoomFactor;
                    }

                    Plotly.update('scatter-plot', {
                        'marker.size': newMarkerSize
                    });
                });
            }
            ,
            error: function (error) {
                console.error('Error parsing CSV:', error);
            }
            ,
        });
    })
    .catch(function (error) {
        console.error('There was a problem with the fetch operation:', error);
    });
