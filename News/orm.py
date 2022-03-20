from db import db

class News(db.Model):
    __tablename__ = 'NEWS'

    NEWS_UUID = db.Column(db.String, primary_key=True)
    NEWS_DAY = db.Column(db.String, nullable=False)
    NEWS_TITLE = db.Column(db.String, nullable=False, convert_unicode=True)
    NEWS_CONTEXT = db.Column(db.String, nullable=False, convert_unicode=True)
    RATING = db.Column(db.Integer, nullable=False)

    def __init__(self, news_day, tag, news_count):
        self.NEWS_UUID = news_day
        self.NEWS_METADATA_KEY = tag
        self.NEWS_METADATA_VALUE = news_count
