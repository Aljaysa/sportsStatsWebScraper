$( "document" ).ready( function setStatsVisAttr(){
    const statsVis = document.getElementById("stats-vis");
    
    fetch('/visualizations/graph?team=white_sox&year=2023&x_axis=age&y_axis=OPSPLUS&graph_type=scatterplot')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); // Print the response text
        statsVis.srcdoc = text; //static/embeddedHTML/statsGraphs/WhiteSox2023AgeVsOPSPLUS.html
        statsVis.title = "Graph: White Sox 2023 Age Vs OPSPLUS";
    });
    
    
});









