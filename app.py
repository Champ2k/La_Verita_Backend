from datetime import datetime
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
import pandas as pd
import re

import ast

from model import *

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


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# # arg = inputword
@app.route("/analysis", methods=["GET"])
def analyze():
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


@app.route("/tweets", methods=["GET", "POST"])
def tweets():
    if request.method == "GET":
        limit_tweet = request.args.get("limit", default=100, type=int)
        hashtag = request.args.get("hashtag", default=None, type=str)
        if hashtag:
            regex = re.compile(hashtag, re.IGNORECASE)

            return jsonify(
                {
                    "tweets": TweetComment.objects(hashtag=regex).limit(
                        limit_tweet
                    )
                }
            )
        else:
            return jsonify({"tweets": TweetComment.objects.limit(limit_tweet)})


@app.route("/addTweets", methods=["GET"])
def addTweets():
    if request.method == "GET":
        loop_range = request.args.get("range", default=10, type=str)
        tweets_data = pd.read_csv("./data/vaccination_tweets_with_sentiment_hashtags.csv")
        df = pd.DataFrame(tweets_data)
        obj_list = []
        for i in range(loop_range):
            sentence = df['text'][i]
            hashtag = tweets_data['hashtag'][i]
            hashtag_to_list = ast.literal_eval(hashtag)
            date = df['date'][i]
            sentiment = df['sentiment'][i]
            tweets_comment = TweetComment(
                comment=sentence, hashtag=hashtag_to_list, date=date, sentiment=sentiment
            )
            tweets_comment.save()
            obj_list.append(tweets_comment)
        return jsonify(obj_list)


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


if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
