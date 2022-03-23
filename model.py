from app import db

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

# class Hashtag(db.Document):
#     hashtag = db.ListField()


class TweetComment(db.Document):
    comment = db.StringField()
    # hashtag = db.ListField(db.ReferenceField(Hashtag))
    hashtag = db.ListField()
    date = db.DateTimeField(required=False)
    user = db.StringField(required=False)
    sentiment = db.StringField()

    def to_json(self):
        return {
            "comment": self.comment,
            "hashtag": self.hashtag,
            "date": self.date,
            "user": self.user,
            "sentiment": self.sentiment,
        }