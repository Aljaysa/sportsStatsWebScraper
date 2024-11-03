from flask import Flask, jsonify, request, render_template, send_file
import visualizer_from_database
from visualizer_from_database import GraphInfo, GraphType

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("visualizations/visualizations.html")

@app.route("/visualizations")
def visualizations():
    return render_template("visualizations/visualizations.html")

@app.route("/the-dev-journey")
def theeDevJourney():
    return render_template("the-dev-journey/the-dev-journey.html")


@app.route('/visualizations/graph', methods=['GET'])
def getVisualizationsGraph():
    if request.method == 'GET':
        try:
            print("got here")
            urlArgs = request.args
            if (urlArgs["graph_type"] == "scatterplot"):
                graphType = GraphType.SCATTERPLOT
                
            if (urlArgs["team"] == "white_sox"):
                team = "White Sox"
            visualizer_from_database.generateGraphHTMLUsingDatabase("baseballStats.db", team, urlArgs["year"], urlArgs["x_axis"], urlArgs["y_axis"], graphType)
            return send_file('static/embeddedHTML/statsGraphs/WhiteSox2023ageVsOPSPLUS.html')
        except Exception as e:
            return str(e)
        
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)