from flask import Flask, render_template, request

import model_file


# Use the model with parameters 
#print(model_file.recommend_crop(30.3279, 19.8190, '01'))

app = Flask(__name__)


@app.route("/")
def idx():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/readypredict")
def readypredict():
    return render_template("readypredict.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/trynow")
def trynow():
    return render_template("findthecrop.html")

@app.route("/prediction", methods=["GET", "POST"])
def predict():
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    month = str(request.form['month'])
    prediction = model_file.recommend_crop(latitude, longitude, month)
    return render_template("prediction.html", result = prediction)

if __name__ == "__main__":
    app.run(debug=True)