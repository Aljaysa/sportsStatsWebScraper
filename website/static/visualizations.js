$( "document" ).ready( function setStatsVisAttr(){
    const statsVis = document.getElementById("stats-vis");
    statsVis.src = "static/embeddedHTML/statsGraphs/WhiteSox2023AgeVsOPSPLUS.html"; 
    statsVis.title = "Graph: White Sox 2023 Age Vs OPSPLUS";
});

//GET
// fetch('/hello')
//     .then(function (response) {
//         return response.text();
//     }).then(function (text) {
//         console.log('GET response text:');
//         console.log(text); // Print the greeting as text
//     });

// POST
fetch('/hello', {

    // Specify the method
    method: 'POST',

    // JSON
    headers: {
        'Content-Type': 'application/json'
    },

    // A JSON payload
    body: JSON.stringify({
        "greeting": "Hello from the browser!"
    })
}).then(function (response) { // At this point, Flask has printed our JSON
    return response.text();
}).then(function (text) {

    console.log('POST response: ');

    // Should be 'OK' if everything was successful
    console.log(text);
});

