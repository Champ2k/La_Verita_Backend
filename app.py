from weakref import ReferenceType
from flask_restful import Api, Resource
import threading
import json
from analyze import (
    filtered_input_vax_base_on_tweets_timeline,
    filtered_all_base_on_tweets_timeline,
)
from classify import analysis
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "super-secret"

# app.config["MONGO_URI"] = "mongodb+srv://poomiix9:poom2542@cluster0.ta2my.mongodb.net/Comment?retryWrites=true&w=majority"
app.config[
    "MONGODB_HOST"
] = "mongodb+srv://poomiix9:poom2542@cluster0.ta2my.mongodb.net/Comment?retryWrites=true&w=majority"

db = MongoEngine()
db.init_app(app)

api = Api(app)

CORS(app)


class AnalysisResult(db.Document):
    result = db.StringField()
    neutral = db.DecimalField(min_value=0, precision=2)
    positive = db.DecimalField(min_value=0, precision=2)
    negative = db.DecimalField(min_value=0, precision=2)
    inputword = db.StringField()

    def to_json(self):
        return {
            "result": self.result,
            "sentiment": {
                "neutral": self.neutral,
                "positive": self.positive,
                "negative": self.negative,
            },
            "inputword": self.inputword,
        }


class Hastag(db.Document):
    hastag = db.StringField()


class TweetComment(db.Document):
    comment = db.StringField()
    hastag = db.ListField(db.ReferenceField(Hastag))
    date = db.DateTimeField(required=False)
    user = db.StringField()
    sentiment = db.StringField()

    def to_json(self):
        return {
            "comment": self.comment,
            "hastag": self.hastag,
            "date": self.date,
            "user": self.user,
            "sentiment": self.sentiment,
        }


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if request.method == "POST":
#         inputword = request.form.get("inputText")
#         result, neutral, positive, negative = analysis(inputword)
#         # analysis_result = AnalysisResult(
#         #     result=result, neutral=neutral, positive=positive, negative=negative, inputword=inputword)
#         # analysis_result.save()
#         # return jsonify(analysis_result.to_json())
#         return render_template("result.html", result=result, neutral=neutral, positive=positive, negative=negative, inputword=inputword)

#     return render_template("home.html")


# arg = inputword
@app.route("/analysis", methods=["GET"])
def get_analyze():
    if request.method == "GET":
        inputword = request.args.get("inputword")
        result, neutral, positive, negative = analysis(inputword)
        analysis_result = AnalysisResult(
            result=result,
            neutral=neutral,
            positive=positive,
            negative=negative,
            inputword=inputword,
        )
        analysis_result.save()
        return jsonify(analysis_result.to_json())


@app.route("/tweets", methods=["GET"])
def get_tweets():
    if request.method == "GET":
        limit_tweet = request.args.get("limit")
        hastag = request.args.get("hastag")

        if limit_tweet and hastag:
            return jsonify(
                {"tweets": AnalysisResult.objects(result__iexact=hastag).limit(int(limit_tweet))}
            )
        elif limit_tweet:
            return jsonify({"tweets": AnalysisResult.limit(int(limit_tweet))})
        elif hastag:
            return jsonify({"tweets": AnalysisResult.objects(result__iexact=hastag).limit(100)})
        else:
            return jsonify({"tweets": AnalysisResult.objects.limit(100)})


# @app.route("/timeline_analysis", methods=['GET'])
# def timeline_analysis():
#     return render_template("timeline_analysis.html")

# plotgraph function in serverside and save pic to static  *** Now Using canvasJs in script to create piechart ***


# def plotgraph(neutral, positive, negative):
#     labels = 'neutral', 'positive', 'negative'
#     sizes = [neutral, positive, negative]
#     explode = (0, 0, 0)
#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, explode=explode, labels=labels,
#             autopct='%1.1f%%', shadow=True, startangle=90)
#     # Equal aspect ratio ensures that pie is drawn as a circle.
#     ax1.axis('equal')
#     plt.savefig('static/images/new_plot.png')


# @app.route("/post_model", methods=['GET'])
# def ClassifyView():
#     tweet = mongo.db.Twitter_Comment
#     tweet.insert_many(books)
#     return "Inserted"

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
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


# class InputTimeline(Resource):
#     def get(self, vax):
#         data = filtered_input_vax_base_on_tweets_timeline(vax)
#         return jsonify(data)


# class Timeline(Resource):
#     def get(self):
#         data = filtered_all_base_on_tweets_timeline()
#         return jsonify(data)

# class Timeline(Resource):
#     def get(self, df):
#         data = filtered_all_vax_base_on_tweets_timeline(df)
#         return jsonify(data)


# api.add_resource(InputTimeline, '/inputtimeline/<vax>')
# api.add_resource(Timeline, '/timeline/<df>')
# api.add_resource(Timeline, '/timeline')

if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
