from flask import Flask, request, jsonify, render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_cors import CORS
from flask_pymongo import PyMongo
from classify import analysis


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://poomiix9:poom2542@cluster0.ta2my.mongodb.net/Comment?retryWrites=true&w=majority"
app.config["DEBUG"] = True
mongo = PyMongo(app)
app.secret_key = "super secret key"
db = mongo.db
CORS(app)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

class ReusableForm(Form):

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        if request.method == "POST":
       # getting input with name = fname in HTML form
            inputword = request.form.get("inputText")
            return analysis(inputword)
       # getting input with name = lname in HTML form 
            
        return render_template("home.html")
       

    @app.route("/post_model", methods=['GET'])
    def ClassifyView():
        tweet = mongo.db.Twitter_Comment
        tweet.insert_many(books)
        return "Inserted"

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
    app.run()

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