from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
import uuid
import time

Base = declarative_base()

class AggregateCategory(Base):
    __tablename__ = 'AGGREGATE_CATEGORY'

    NEWS_DAY = Column(String, primary_key=True)
    DAY_OF_WEEK = Column(String, nullable=False)
    SORT_YEAR = Column(String, nullable=False)
    SORT_MONTH = Column(String, nullable=False)
    SORT_DAY = Column(String, nullable=False)
    CATEGORY = Column(String, primary_key=True)
    NEWS_COUNT = Column(Integer, nullable=False)

    def __init__(self, news_day, week_day, category, news_count):
        self.NEWS_DAY = news_day
        self.DAY_OF_WEEK = week_day
        self.SORT_YEAR = time.strftime("%Y", time.strptime(news_day, "%Y%m%d"))
        self.SORT_MONTH = time.strftime("%m", time.strptime(news_day, "%Y%m%d"))
        self.SORT_DAY = time.strftime("%d", time.strptime(news_day, "%Y%m%d"))
        self.CATEGORY = category
        self.NEWS_COUNT = news_count

class AggregateSentiment(Base):
    __tablename__ = 'AGGREGATE_SENTIMENT'

    NEWS_DAY = Column(String, primary_key=True)
    DAY_OF_WEEK = Column(String, nullable=False)
    SORT_YEAR = Column(String, nullable=False)
    SORT_MONTH = Column(String, nullable=False)
    SORT_DAY = Column(String, nullable=False)
    SENTIMENT = Column(String, primary_key=True, nullable=False)
    NEWS_COUNT = Column(Integer, nullable=False)

    def __init__(self, news_day, week_day, sentiment, news_count):
        self.NEWS_DAY = news_day
        self.DAY_OF_WEEK = week_day
        self.SORT_YEAR = time.strftime("%Y", time.strptime(news_day, "%Y%m%d"))
        self.SORT_MONTH = time.strftime("%m", time.strptime(news_day, "%Y%m%d"))
        self.SORT_DAY = time.strftime("%d", time.strptime(news_day, "%Y%m%d"))
        self.SENTIMENT = sentiment
        self.NEWS_COUNT = news_count

class AggregateTopic(Base):
    __tablename__ = 'AGGREGATE_TOPIC'

    NEWS_DAY = Column(String, primary_key=True)
    DAY_OF_WEEK = Column(String, nullable=False)
    SORT_YEAR = Column(String, nullable=False)
    SORT_MONTH = Column(String, nullable=False)
    SORT_DAY = Column(String, nullable=False)
    TOPIC = Column(String, primary_key=True)
    NEWS_COUNT = Column(Integer, nullable=False)

    def __init__(self, news_day, week_day, topic, news_count):
        self.NEWS_DAY = news_day
        self.DAY_OF_WEEK = week_day
        self.SORT_YEAR = time.strftime("%Y", time.strptime(news_day, "%Y%m%d"))
        self.SORT_MONTH = time.strftime("%m", time.strptime(news_day, "%Y%m%d"))
        self.SORT_DAY = time.strftime("%d", time.strptime(news_day, "%Y%m%d"))
        self.TOPIC = topic
        self.NEWS_COUNT = news_count

class AggregateTag(Base):
    __tablename__ = 'AGGREGATE_TAG'

    NEWS_DAY = Column(String, primary_key=True)
    DAY_OF_WEEK = Column(String, nullable=False)
    SORT_YEAR = Column(String, nullable=False)
    SORT_MONTH = Column(String, nullable=False)
    SORT_DAY = Column(String, nullable=False)
    TAG = Column(String, primary_key=True)
    NEWS_COUNT = Column(Integer, nullable=False)

    def __init__(self, news_day, week_day, tag, news_count):
        self.NEWS_DAY = news_day
        self.DAY_OF_WEEK = week_day
        self.SORT_YEAR = time.strftime("%Y", time.strptime(news_day, "%Y%m%d"))
        self.SORT_MONTH = time.strftime("%m", time.strptime(news_day, "%Y%m%d"))
        self.SORT_DAY = time.strftime("%d", time.strptime(news_day, "%Y%m%d"))
        self.TAG = tag
        self.NEWS_COUNT = news_count


class News(Base):
    __tablename__ = 'NEWS'

    NEWS_UUID = Column(String, primary_key=True)
    NEWS_DAY = Column(String, nullable=False)
    DAY_OF_WEEK = Column(String, nullable=False)
    NEWS_TITLE = Column(String, nullable=False)
    CATEGORY = Column(String, nullable=False)
    NEWS_ABSTRACT = Column(LONGTEXT, nullable=False)
    NEWS_CONTEXT = Column(LONGTEXT, nullable=False)

    def __init__(self, news_uuid, news_day, week_day, title, context, category):
        self.NEWS_UUID = news_uuid
        self.DAY_OF_WEEK = week_day
        self.NEWS_DAY = news_day
        self.NEWS_TITLE = title
        self.NEWS_CONTEXT = context
        self.NEWS_ABSTRACT = context.split(' ')[:30]
        self.CATEGORY = category

class NewsMap(Base):
    __tablename__ = 'NEWS_MAP'
    NEWS_MAP_UUID = Column(String, primary_key=True)
    NEWS_UUID = Column(String, ForeignKey('NEWS.NEWS_UUID'), nullable=False)
    NEWS_DAY = Column(String, nullable=False)
    DAY_OF_WEEK = Column(String, nullable=False)
    NEWS_METADATA_KEY = Column(String, nullable=False)
    NEWS_METADATA_VALUE = Column(String, nullable=False)

    def __init__(self, news_uuid, news_day, week_day, news_metadata_key, news_metadata_value):
        self.NEWS_MAP_UUID = str(uuid.uuid4())
        self.NEWS_UUID = news_uuid
        self.DAY_OF_WEEK = week_day
        self.NEWS_DAY = news_day
        self.NEWS_METADATA_KEY = news_metadata_key
        self.NEWS_METADATA_VALUE = news_metadata_value
