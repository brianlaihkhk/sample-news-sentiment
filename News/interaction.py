import response
from orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, AggregateInteraction, News, NewsMap
from sqlalchemy import or_, and_, func, text
from query import Query

class Interaction:
    def __init__(self, db):
        self.db_connection = db
        self.query_limit = 50
        self.query = Query(db)

    def add_news_rating(self, uuid, rating):
        if abs(rating) > 1 :
            raise Exception("rating cannot greater than 1")

        news = self.query.get_set_news(uuid)
        news_metadata = self.query.get_set_news_map(uuid)

        news.RATING += 1
        self.populate_metadata(news, news_metadata)

        self.db_connection.session.commit()

    def populate_metadata(self, news, news_metadata):
        self.add_metadata_popularity(AggregateCategory, [ news.NEWS_DAY ], AggregateCategory.CATEGORY, [ news.CATEGORY ] )

        self.add_metadata_popularity(AggregateTag, [ news.NEWS_DAY ], AggregateTag.TAG, [ str(row.NEWS_METADATA_VALUE) for row in news_metadata if row.NEWS_METADATA_KEY == 'tag'])

        self.add_metadata_popularity(AggregateSentiment, [ news.NEWS_DAY ], AggregateSentiment.SENTIMENT, [ str(row.NEWS_METADATA_VALUE) for row in news_metadata if row.NEWS_METADATA_KEY == 'sentiment'])

        self.add_metadata_popularity(AggregateTopic, [ news.NEWS_DAY ], AggregateTopic.TOPIC, [ str(row.NEWS_METADATA_VALUE) for row in news_metadata if row.NEWS_METADATA_KEY == 'topic'])

    def add_metadata_popularity(self, orm_class, news_day_list = None, metadata_key = None, metadata_value_list = None):
        result_list = self.query.get_set_metadata(orm_class, news_day_list, metadata_key, metadata_value_list)
        for result in result_list:
            result.POPULARITY += 1
        self.db_connection.session.commit()
