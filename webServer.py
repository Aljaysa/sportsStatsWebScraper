from flask import Flask, jsonify, request, render_template, send_file
import visualizer_from_database
from visualizer_from_database import GraphInfo, GraphType, DatabaseUpdateFailedException
import traceback
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this script

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this script
DB_FILENAME = "baseballStats.db"
databaseName = os.path.join(BASE_DIR, DB_FILENAME)
#databaseName = "baseballStats.db"
urlArgToGraphTypeBindings = dict([
    ("scatterplot", GraphType.SCATTERPLOT),
])

@app.route("/")
def home():
    return render_template("visualizations/visualizations.html")

@app.route("/visualizations")
def visualizations():
    return render_template("visualizations/visualizations.html")

@app.route("/the-dev-journey")
def theDevJourney():
    return render_template("the-dev-journey/the-dev-journey.html")


@app.route('/visualizations/graph', methods=['GET'])
def getVisualizationsGraph():
    if request.method == 'GET':
        try:
            print("Database path:", databaseName)
            print("DB file exists:", os.path.exists(databaseName))
            urlArgs = request.args
            visualizer_from_database.generateGraphHTMLUsingUpdatedDatabase(databaseName, teamNameUrlArgFormatToWebServerFormat(urlArgs["team"]), urlArgs["year"], urlArgs["x_axis"],urlArgs["y_axis"], urlArgToGraphTypeBindings[urlArgs["graph_type"]])
            graphFileName = visualizer_from_database.getGraphHTMLFileName(GraphInfo(teamNameUrlArgFormatToWebServerFormat(urlArgs["team"]), urlArgs["year"], urlArgs["x_axis"] ,urlArgs["y_axis"], urlArgToGraphTypeBindings[urlArgs["graph_type"]]))
            return send_file(graphFileName)
        except DatabaseUpdateFailedException as e:
            traceback.print_exc()
            return returnGeneratedGraphHTMLUsingNonUpdatedDatabase(urlArgs)
        except Exception as e:
            traceback.print_exc()
            errorMsg = traceback.format_exc()
            return str(errorMsg)
        
def returnGeneratedGraphHTMLUsingNonUpdatedDatabase(urlArgs):
    try:
        graphFileName = visualizer_from_database.getGraphHTMLFileName(GraphInfo(teamNameUrlArgFormatToWebServerFormat(urlArgs["team"]), urlArgs["year"], urlArgs["x_axis"], urlArgs["y_axis"], urlArgToGraphTypeBindings[urlArgs["graph_type"]]))
        visualizer_from_database.generateGraphHTMLUsingNonUpdatedDatabase(databaseName, teamNameUrlArgFormatToWebServerFormat(urlArgs["team"]), urlArgs["year"], urlArgs["x_axis"], urlArgs["y_axis"], urlArgToGraphTypeBindings[urlArgs["graph_type"]])
        return send_file(graphFileName)
    except:
        traceback.print_exc()
        errorMsg = traceback.format_exc()
        return str(errorMsg)
    
def teamNameUrlArgFormatToWebServerFormat(urlArgFormattedTeam):
    teamWords = urlArgFormattedTeam.split("_")
    webServerFormattedTeam = ""
    for idx, word in enumerate(teamWords):
        if(idx >= 1): #want to add spaces to separate words (ex: "Red Sox") but the first word should not have a space in front of it 
            webServerFormattedTeam = webServerFormattedTeam + " "
        webServerFormattedTeam = webServerFormattedTeam + word.capitalize()
    return webServerFormattedTeam

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)