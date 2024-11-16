$( "document" ).ready( function setStatsVisAttr(){
    const statsVis = document.getElementById("stats-vis");
    
});

function displayBaseballVisGraph(){
    const userParams = new FormData(document.getElementById("stats-graph-user-parms"));
    userParams.delete("position");
    
    
    const urlOfRequest = "/visualizations/graph" + getGraphURLParamsToRequestFromServer(Object.fromEntries(userParams), "scatterplot"); //'/visualizations/graph?team=blue_jays&year=2022&x_axis=age&y_axis=OPSPLUS&graph_type=scatterplot'

    getGraphFromServerAndDisplay("stats-vis", urlOfRequest);
}

function getGraphURLParamsToRequestFromServer(userParams, graphType){ 
    let urlParamsToRequestFromServer = "?" + (new URLSearchParams(userParams)).toString();
    // for(const pair of userParams.entries()){ // I found out that there is a function out there that exists and does this already for me
    //     urlParamsToRequestFromServer = urlParamsToRequestFromServer.concat(pair[0], "=", pair[1], "&");
    // }
    urlParamsToRequestFromServer = urlParamsToRequestFromServer.concat("&graph_type=", graphType);
    return urlParamsToRequestFromServer;
}


function getGraphFromServerAndDisplay(graphId, urlOfRequest){
    const statsVis = document.getElementById(graphId);
    try {
        fetch(urlOfRequest)
        .then(function (response) {
            return response.text();
        }).then(function (text) {
            console.log('GET response text:');
            console.log(text); // Print the response text
            statsVis.srcdoc = text; //static/embeddedHTML/statsGraphs/WhiteSox2023AgeVsOPSPLUS.html
        }); 
    } catch (e) {
        console.error(e);
    }
}









