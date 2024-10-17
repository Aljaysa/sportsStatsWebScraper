function setStatsVisAttr(){
    var statsVis = document.getElementById("stats-vis");
    statsVis.src = "..\..\embeddedHTML\statsGraphs\WhiteSox2023AgeVsOPSPLUS.html";

    statsVis.title = "Graph: White Sox 2023 Age Vs OPSPLUS" 
}

fetch('/hello')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); // Print the greeting as text
    });

setStatsVisAttr();
