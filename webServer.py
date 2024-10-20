from flask import Flask, jsonify, request, render_template
from visualizer_from_database import VisualizerFromDatabase

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
            message = {'greeting':request.full_path.split("?", 1)[1]}
            
            return jsonify(message)  # serialize and use JSON headers
        except:
            return "/visualizations/graph GET request does not contain arguments as expected"
        
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)