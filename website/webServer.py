from flask import Flask, jsonify, request, render_template

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


@app.route('/hello', methods=['GET', 'POST'])
def visualizationsMethods():
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'OK', 200

# GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)