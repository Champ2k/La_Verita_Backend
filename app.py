import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_cors import CORS
from flask_pymongo import PyMongo
from classify import analysis
from analyze import filtered_input_vax_base_on_tweets_timeline
import json
import threading


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://poomiix9:poom2542@cluster0.ta2my.mongodb.net/Comment?retryWrites=true&w=majority"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["DEBUG"] = True
mongo = PyMongo(app)
app.secret_key = "super secret key"
db = mongo.db
CORS(app)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        inputword = request.form.get("inputText")
        result,neutral,positive,negative = analysis(inputword)
        data = {}
        return render_template("result.html", result=result, neutral=neutral, positive=positive, negative=negative, url="static/images/new_plot.png")
        
    return render_template("home.html")

# plotgraph function in serverside and save pic to static  *** Now Using canvasJs in script to create piechart ***
def plotgraph(neutral,positive,negative):
    labels = 'neutral','positive','negative'
    sizes = [neutral,positive,negative]
    explode = (0, 0, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('static/images/new_plot.png')


@app.route("/post_model", methods=['GET'])
def ClassifyView():
    tweet = mongo.db.Twitter_Comment
    tweet.insert_many(books)
    return "Inserted"

# No caching at all for API endpoints.
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/api/analyze/", methods=['GET'])
def analyze():
    data = filtered_input_vax_base_on_tweets_timeline('sinovac')
    return  data
    
# def ClassifyView():

# star = mongo.db.stars
#   name = request.json['name']
#   distance = request.json['distance']
#   star_id = star.insert({'name': name, 'distance': distance})
#   new_star = star.find_one({'_id': star_id })
#   output = {'name' : new_star['name'], 'distance' : new_star['distance']}
#   return jsonify({'result' : output})


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)

# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]

# A route to return all of the available entries in our catalog.
# @app.route('/api/book', methods=['GET'])
# def api_all():
#     return jsonify(books)