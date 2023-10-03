var csvFilePath = 'data/umap_visualization.csv';
var traces;
var parsedData;

function closeInfoBox() {
    infoBox.style.display = 'none';
}

function searchName() {
    var searchInput = document.getElementById("nameSearchInput").value;
    if (searchInput.length < 3) {
        alert("Please enter at least 3 letters to search.");
        return;
    }

    traces = [];
    var isFoundAnything = false

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
                citation: row["Citation"],
                acmProfile: row["ACM Fellow Profile"],
                googleScholarProfile: row["Google Scholar Profile"],
                dblpProfile: row["DBLP profile"],
                imgProfile: row["image_url"]
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
                size: customDataArray.map(row => row.name.toLowerCase().includes(searchInput.toLowerCase()) ? 15 : 7),
                colorscale: 'Jet',
            },
            type: 'scatter',
            name: 'Cluster ' + i
        };

        trace.marker.color = customDataArray.map(row => {
            if (row.name.toLowerCase().includes(searchInput.toLowerCase())) {
                isFoundAnything = true
                return 'rgba(0, 0, 255, 1)';
            } else {
                return 'rgba(0,0,0,0.30)';
            }
        });

        traces.push(trace);
    }

    if (!isFoundAnything) {
        alert("No matching data found for the given search input.");
        return;
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
        plot_bgcolor: '#FDF7F0',
        dragmode: 'pan'
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
            responsive: true,
        }
    );

    var plotContainer = document.getElementById('scatter-plot');

    traces.forEach(function (trace, i) {

        trace.customdata.forEach(function (dataObj) {
            dataObj.traceNumber = i;
        });
    });

    var infoBox = document.getElementById('infoBox');

    plotContainer.on('plotly_click', function (eventData) {
        infoBox.style.display = 'none'

        var pointIndex = eventData.points[0].pointIndex;
        var selectedData = eventData.points[0].customdata;
        var traceNumber = selectedData.traceNumber;

        document.getElementById('name').textContent = selectedData.name;
        document.getElementById('citation').textContent = selectedData.citation;
        document.getElementById('cluster').textContent = '' + (traceNumber + 1);
        document.getElementById('keywords').textContent = traces[traceNumber].text[pointIndex];

        function updateProfileLink(id, sectionId, profileData) {
            var element = document.getElementById(id);
            var section = document.getElementById(sectionId);

            if (profileData) {
                element.href = profileData;
                element.style.display = 'inline-block';
                section.style.display = 'inline-block';
            } else {
                element.style.display = 'none';
                section.style.display = 'none';
            }
        }

        updateProfileLink('googleScholarProfile', 'googleScholarSection', selectedData.googleScholarProfile);
        updateProfileLink('acmProfile', 'acmSection', selectedData.acmProfile);
        updateProfileLink('dblpProfile', 'dblpSection', selectedData.dblpProfile);

        var imageElement = document.getElementById('image');
        var imageSection = document.getElementById('imageSection');

        if (selectedData.imgProfile && selectedData.imgProfile !== 'nan') {
            imageSection.style.display = 'block'
            imageElement.src = selectedData.imgProfile;
            imageElement.style.display = 'block';
        } else {
            imageSection.style.display = 'none'
            imageElement.style.display = 'none';
        }

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

                    parsedData = results.data;
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
                                citation: row["Citation"],
                                acmProfile: row["ACM Fellow Profile"],
                                googleScholarProfile: row["Google Scholar Profile"],
                                dblpProfile: row["DBLP profile"],
                                imgProfile: row["image_url"]
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
                                size: 7,
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
                        plot_bgcolor: '#FDF7F0',
                        dragmode: 'pan'
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
                            responsive: true,
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
                        infoBox.style.display = 'none'

                        var pointIndex = eventData.points[0].pointIndex;
                        var selectedData = eventData.points[0].customdata;
                        var traceNumber = selectedData.traceNumber;

                        document.getElementById('name').textContent = selectedData.name;
                        document.getElementById('citation').textContent = selectedData.citation;
                        document.getElementById('cluster').textContent = '' + (traceNumber + 1);
                        document.getElementById('keywords').textContent = traces[traceNumber].text[pointIndex];

                        function updateProfileLink(id, sectionId, profileData) {
                            var element = document.getElementById(id);
                            var section = document.getElementById(sectionId);

                            if (profileData) {
                                element.href = profileData;
                                element.style.display = 'inline-block';
                                section.style.display = 'inline-block';
                            } else {
                                element.style.display = 'none';
                                section.style.display = 'none';
                            }
                        }

                        updateProfileLink('googleScholarProfile', 'googleScholarSection', selectedData.googleScholarProfile);
                        updateProfileLink('acmProfile', 'acmSection', selectedData.acmProfile);
                        updateProfileLink('dblpProfile', 'dblpSection', selectedData.dblpProfile);

                        var imageElement = document.getElementById('image');
                        var imageSection = document.getElementById('imageSection');

                        if (selectedData.imgProfile && selectedData.imgProfile !== 'nan') {
                            imageSection.style.display = 'block'
                            imageElement.src = selectedData.imgProfile;
                            imageElement.style.display = 'block';
                        } else {
                            imageSection.style.display = 'none'
                            imageElement.style.display = 'none';
                        }

                        infoBox.style.display = 'block';
                    });

                    // plotContainer.on('plotly_relayout', function (eventData) {
                    //     var zoomFactor = eventData['xaxis.range[1]'] - eventData['xaxis.range[0]'];
                    //     if (isNaN(zoomFactor)) {
                    //         newMarkerSize = 10
                    //     } else if (zoomFactor < 6) {
                    //         var newMarkerSize = 10 / zoomFactor;
                    //     }
                    //
                    //     Plotly.update('scatter-plot', {
                    //         'marker.size': newMarkerSize
                    //     });
                    // });
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