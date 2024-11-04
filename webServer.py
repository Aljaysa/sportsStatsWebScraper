from flask import Flask, jsonify, request, render_template, send_file
import visualizer_from_database
from visualizer_from_database import GraphInfo, GraphType, DatabaseUpdateFailedException
import traceback


app = Flask(__name__)

databaseName = "baseballStats.db"


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
            urlArgs = request.args
            if (urlArgs["graph_type"] == "scatterplot"):
                graphType = GraphType.SCATTERPLOT
                
            if (urlArgs["team"] == "white_sox"):
                team = "White Sox"
            visualizer_from_database.generateGraphHTMLUsingUpdatedDatabase(databaseName, team, urlArgs["year"], urlArgs["x_axis"], urlArgs["y_axis"], graphType)
            return send_file('static/embeddedHTML/statsGraphs/Yankees2023ageVsOPSPLUS.html')
        except DatabaseUpdateFailedException as e:
            traceback.print_exc()
            returnGenerateGraphHTMLUsingNonUpdatedDatabase(team, urlArgs, graphType)
        except Exception as e:
            traceback.print_exc()
            errorMsg = traceback.format_exc()
            return str(errorMsg)
        
def returnGenerateGraphHTMLUsingNonUpdatedDatabase(team, urlArgs, graphType):
    try:
        visualizer_from_database.generateGraphHTMLUsingNonUpdatedDatabase(databaseName, team, urlArgs["year"], urlArgs["x_axis"], urlArgs["y_axis"], graphType)
        return send_file('static/embeddedHTML/statsGraphs/Yankees2023ageVsOPSPLUS.html')
    except:
        traceback.print_exc()
        errorMsg = traceback.format_exc()
        return str(errorMsg)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)