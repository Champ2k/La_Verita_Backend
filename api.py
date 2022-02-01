from app import app
from flask import request, jsonify
from model import *
from classify import analysis

# arg = inputword
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
            return jsonify(
                {
                    "tweets": TweetComment.objects(hashtag__iexact=hashtag).limit(
                        limit_tweet
                    )
                }
            )
        else:
            return jsonify({"tweets": TweetComment.objects.limit(limit_tweet)})