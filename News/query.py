import response
from orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, AggregateInteraction, News, NewsMap
from db import Database
from sqlalchemy import or_, and_, func, text

class Query:
    def __init__(self):
        self.db_connection = Database().db
        self.query_limit = 50

    def get_news(self, event) :
        query_parameter = self.get_news_parameter(event, News)

        news_result = self.db_connection.session.query(News).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        result = [ dict(zip(query_parameter.get('key'), row)) for row in news_result]

        if len(news_result) == 1 and (event.get('query').get('NEWS_UUID') is not None) :

            map_query_parameter = self.get_news_map_parameter(event, NewsMap)
            news_map_result = self.db_connection.session.query(NewsMap).with_entities(*map_query_parameter.get('with_entities')).filter(and_(*map_query_parameter.get('filter'))).all()
            result = {'news' : result[0], 'metadata' : [ dict(zip(map_query_parameter.get('key'), row)) for row in news_map_result]}

        return result

    def update_news_count(self, news):
        news.POPULARITY += 1
        self.db_connection.session.commit()

    def update_category_count(self, category_list):
        for category in category_list:
            category.POPULARITY += 1
        self.db_connection.session.commit()

    def get_category(self, event) :
        query_parameter = self.get_query_parameter(event, AggregateCategory)

        category_result = self.db_connection.session.query(AggregateCategory).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in category_result]

    def update_topic_count(self, topic_list):
        for topic in topic_list:
            topic.POPULARITY += 1
        self.db_connection.session.commit()


    def get_topic(self, event) :
        query_parameter = self.get_query_parameter(event, AggregateTopic)

        topic_result = self.db_connection.session.query(AggregateTopic).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in topic_result]


    def update_tag_count(self, tag_list):
        for tag in tag_list:
            tag.POPULARITY += 1
        self.db_connection.session.commit()

    def get_tag(self, event) :
        query_parameter = self.get_query_parameter(event, AggregateTag)

        tag_result = self.db_connection.session.query(AggregateTag).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in tag_result]


    def update_sentiment_count(self, sentiment_list):
        for sentiment in sentiment_list:
            sentiment.POPULARITY += 1
        self.db_connection.session.commit()

    def get_sentiment(self, event) :
        query_parameter = self.get_query_parameter(event, AggregateSentiment)

        sentiment_result = self.db_connection.session.query(AggregateSentiment).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in sentiment_result]

    def get_news_parameter (self, event, orm_class):
        with_entities = [orm_class.NEWS_UUID, orm_class.NEWS_DAY, orm_class.NEWS_TITLE, orm_class.NEWS_CONTEXT, orm_class.CATEGORY, orm_class.RATING, orm_class.POPULARITY]
        order_by = []
        filter = []
        key = ['uuid', 'news_day', 'news_title', 'news_context', 'category', 'rating', 'popularity']

        if event.get('query').get('NEWS_UUID'):
            filter.append(orm_class.NEWS_UUID.like(event.get('query').get('NEWS_UUID')))
        if event.get('query').get('CATEGORY'):
            filter.append(orm_class.CATEGORY.like(event.get('query').get('CATEGORY')))
            order_by.append(orm_class.POPULARITY.desc())

        return { 'with_entities' : with_entities, 'filter' : filter, 'key' : key, 'order_by' : order_by }

    def get_news_map_parameter (self, event, orm_class):
        with_entities = [orm_class.NEWS_METADATA_KEY, orm_class.NEWS_METADATA_VALUE]
        filter = []
        key = ['key', 'value']

        if event.get('query').get('NEWS_UUID'):
            filter.append(orm_class.NEWS_UUID.like(event.get('query').get('NEWS_UUID')))

        return { 'with_entities' : with_entities, 'filter' : filter, 'key' : key }

    def get_query_parameter (self, event, orm_class):
        group_by = []
        with_entities = [ func.count(orm_class.POPULARITY).label('POPULARITY') ]
        filter = []
        order_by = [ text('POPULARITY desc') ]
        key = ['popularity']

        if event.get('query').get('DATE'):
            filter.append(orm_class.NEWS_DAY.like(event.get('query').get('DATE')))

        if event.get('query').get('WEEK_DAY'):
            filter.append(orm_class.DAY_OF_WEEK.like(event.get('query').get('WEEK_DAY')))
            group_by.append(orm_class.DAY_OF_WEEK)
            with_entities.append(orm_class.DAY_OF_WEEK)
            key.append('week_day')

        if event.get('query').get('YEAR'):
            group_by.append(orm_class.SORT_YEAR)
            with_entities.append(orm_class.SORT_YEAR)
            key.append('year')

        if event.get('query').get('MONTH'):
            group_by.append(orm_class.SORT_MONTH)
            with_entities.append(orm_class.SORT_MONTH)
            key.append('month')

        if event.get('query').get('DAY'):
            group_by.append(orm_class.SORT_DAY)
            with_entities.append(orm_class.SORT_DAY)
            key.append('day')

        if event.get('query').get('CATEGORY'):
            group_by.append(orm_class.CATEGORY)
            with_entities.append(orm_class.CATEGORY)
            filter.append(orm_class.CATEGORY.like(event.get('query').get('CATEGORY')))
            key.append('category')

        if event.get('query').get('TAG'):
            group_by.append(orm_class.TAG)
            with_entities.append(orm_class.TAG)
            filter.append(orm_class.TAG.like(event.get('query').get('TAG')))
            key.append('tag')

        if event.get('query').get('SENTIMENT'):
            group_by.append(orm_class.SENTIMENT)
            with_entities.append(orm_class.SENTIMENT)
            filter.append(orm_class.SENTIMENT.like(event.get('query').get('SENTIMENT')))
            key.append('sentiment')

        if event.get('query').get('TOPIC'):
            group_by.append(orm_class.TOPIC)
            with_entities.append(orm_class.TOPIC)
            filter.append(orm_class.TOPIC.like(event.get('query').get('TOPIC')))
            key.append('topic')

        return { 'group_by' : group_by , 'with_entities' : with_entities, 'filter' : filter, 'key' : key, 'order_by' : order_by }