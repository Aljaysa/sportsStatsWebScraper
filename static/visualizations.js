$( "document" ).ready( function setStatsVisAttr(){
    const statsVis = document.getElementById("stats-vis");
    
    
    
    statsVis.src = "static/embeddedHTML/statsGraphs/WhiteSox2023AgeVsOPSPLUS.html"; //static/embeddedHTML/statsGraphs/WhiteSox2023AgeVsOPSPLUS.html
    statsVis.title = "Graph: White Sox 2023 Age Vs OPSPLUS";
});

fetch('/visualizations/graph?graph-type=scatterplot&x-axis=OPSPLUS')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); // Print the response text
    });



