from datetime import datetime
from unittest import result
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
import urllib.parse

import ast

from model import *

matplotlib.use("Agg")
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "super-secret"

app.config[
    "MONGODB_HOST"
] = "URL to connect to your data base"

db = MongoEngine()
db.init_app(app)


api = Api(app)

CORS(app)


def countOverallSentiment(list):
    countNeutral = 0
    countPositive = 0
    countNegative = 0

    for i in range(len(list)):
        sentiment = list[i].sentiment.lower()
        if sentiment == "neutral":
            countNeutral += 1
        elif sentiment == "positive":
            countPositive += 1
        elif sentiment == "negative":
            countNegative += 1
    return countNeutral, countPositive, countNegative


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
                {"tweets": TweetComment.objects(hashtag=regex).limit(limit_tweet)}
            )
        else:
            return jsonify({"tweets": TweetComment.objects.limit(limit_tweet)})


@app.route("/addTweets", methods=["GET"])
def addTweets():
    if request.method == "GET":
        loop_range = request.args.get("range", default=10, type=int)
        tweets_data = pd.read_csv(
            "./data/vaccination_tweets_with_sentiment_hashtags.csv"
        )
        df = pd.DataFrame(tweets_data)
        obj_list = []
        for i in range(loop_range):
            sentence = df["text"][i]
            hashtag = tweets_data["hashtag"][i]
            hashtag_to_list = ast.literal_eval(hashtag)
            date = df["date"][i]
            # sentiment = df["sentiment"][i]
            result, neutral, positive, negative = analysis(df["text"][i])
            tweets_comment = TweetComment(
                comment=sentence,
                hashtag=hashtag_to_list,
                date=date,
                sentiment=result,
            )
            tweets_comment.save()
            obj_list.append(tweets_comment)
        return jsonify(obj_list)


@app.route("/countOverallSentiment", methods=["GET"])
def countOverallSentiment():
    if request.method == "GET":
        hashtag = request.args.get("hashtag", default=None, type=str)
        if hashtag:
            regex = re.compile(hashtag, re.IGNORECASE)

            listObjTweets = TweetComment.objects(hashtag=regex)
        else:
            listObjTweets = TweetComment.objects()

        neu, pos, neg = countOverallSentiment(listObjTweets)
        overallSentiment = OverallSentiment(
            hashtag=hashtag if hashtag else "all",
            countTweet=len(listObjTweets),
            countPositive=pos,
            countNegative=neg,
            countNeutral=neu,
        )
        overallSentiment.save()
        return jsonify(overallSentiment.to_json())

@app.route("/getOverallSentiment", methods=["GET"])
def getOverallSentiment():
    if request.method == "GET":
        hashtag = request.args.get("hashtag", default="all", type=str)
        regex = re.compile(hashtag, re.IGNORECASE)
        listObjTweets = OverallSentiment.objects(hashtag=regex)
        return jsonify(listObjTweets)


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
