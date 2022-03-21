import response
from orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, News, NewsMap
from sqlalchemy import or_, and_, func, text

class Query:
    def __init__(self, db):
        self.db_connection = db
        self.query_limit = 200

    def get_set_news (self, uuid = None, category = None):
        filter = {}
        if uuid:
            filter.update({'NEWS_UUID': uuid})
        if category:
            filter.update({'CATEGORY': category})
        return self.db_connection.session.query(News).filter_by(**filter).first()

    def get_set_news_map (self, uuid = None):
        filter = {}
        if uuid:
            filter.update({'NEWS_UUID': uuid})
        return self.db_connection.session.query(NewsMap).filter_by(**filter).all()

    def get_set_metadata (self, orm_class, news_day_list = None, metadata_key = None, metadata_value_list = None):
        filter = []
        if news_day_list:
            filter.append(orm_class.NEWS_DAY.in_(news_day_list))
        if metadata_key and metadata_value_list:
            filter.append(metadata_key.in_(metadata_value_list))
        return self.db_connection.session.query(orm_class).filter(and_(*filter)).all()

    def get_news(self, criteria) :
        query_parameter = self.get_news_parameter(criteria, News)

        news_result = self.db_connection.session.query(News).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        result = [ dict(zip(query_parameter.get('key'), row)) for row in news_result]

        if len(news_result) == 1 and (criteria.get('NEWS_UUID') is not None) :

            map_query_parameter = self.get_news_map_parameter(criteria, NewsMap)
            print(map_query_parameter)
            news_map_result = self.db_connection.session.query(NewsMap).with_entities(*map_query_parameter.get('with_entities')).filter(and_(*map_query_parameter.get('filter'))).all()

            result = {'news' : result, 'metadata' : [ dict(zip(map_query_parameter.get('key'), row)) for row in news_map_result]}

        return result

    def get_search(self, criteria) :
        news_criteria = criteria.copy()
        news_uuid_list = ['dummy']

        if not (criteria.get('CATEGORY_LIST') or criteria.get('CATEGORY')) :
            criteria.update({'NEWS_UUID' : '%'})

            map_query_parameter = self.get_news_map_parameter(criteria, NewsMap)

            news_map_result = self.db_connection.session.query(NewsMap).with_entities(*map_query_parameter.get('with_entities')).filter(and_(*map_query_parameter.get('filter'))).all()
            result_set = [ dict(zip(map_query_parameter.get('key'), row)) for row in news_map_result]

            news_criteria.update({'NEWS_UUID_LIST' : news_uuid_list + [ row['uuid'] for row in result_set]})
        else:
            news_criteria.update({'NEWS_UUID' : '%'})

        query_parameter = self.get_news_parameter(news_criteria, News)

        news_result = self.db_connection.session.query(News).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in news_result]

    def get_category(self, criteria) :
        query_parameter = self.get_metadata_parameter(criteria, AggregateCategory, AggregateCategory.CATEGORY, 'category')

        category_result = self.db_connection.session.query(AggregateCategory).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in category_result]

    def get_topic(self, criteria) :
        query_parameter = self.get_metadata_parameter(criteria, AggregateTopic, AggregateTopic.TOPIC, 'topic')

        topic_result = self.db_connection.session.query(AggregateTopic).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in topic_result]

    def get_tag(self, criteria) :
        query_parameter = self.get_metadata_parameter(criteria, AggregateTag, AggregateTag.TAG, 'tag')

        tag_result = self.db_connection.session.query(AggregateTag).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in tag_result]

    def get_sentiment(self, criteria) :
        query_parameter = self.get_metadata_parameter(criteria, AggregateSentiment, AggregateSentiment.SENTIMENT, 'sentiment')

        sentiment_result = self.db_connection.session.query(AggregateSentiment).with_entities(*query_parameter.get('with_entities')).filter(and_(*query_parameter.get('filter'))).group_by(*query_parameter.get('group_by')).order_by(*query_parameter.get('order_by')).limit(self.query_limit).all()

        return [ dict(zip(query_parameter.get('key'), row)) for row in sentiment_result]

    def get_news_parameter (self, criteria, orm_class):
        with_entities = []
        order_by = []
        filter = []
        key = []
        group_by = []
        require_base = True

        if criteria.get('NEWS_UUID') or criteria.get('NEWS_UUID_LIST'):
            if criteria.get('NEWS_UUID'):
                filter.append(orm_class.NEWS_UUID.like(criteria.get('NEWS_UUID')))
            if criteria.get('NEWS_UUID_LIST'):
                filter.append(orm_class.NEWS_UUID.in_(criteria.get('NEWS_UUID_LIST')))

            with_entities.append(orm_class.NEWS_CONTEXT)
            key.append('news_context')
            with_entities.append(orm_class.NEWS_UUID)
            key.append('uuid')
            with_entities.append(orm_class.NEWS_DAY)
            key.append('news_day')
            with_entities.append(orm_class.NEWS_TITLE)
            key.append('news_title')
            with_entities.append(orm_class.NEWS_ABSTRACT)
            key.append('news_abstract')
            with_entities.append(orm_class.CATEGORY)
            key.append('category')
            require_base = False

        if criteria.get('DATE'):
            filter.append(orm_class.NEWS_DAY.like(criteria.get('DATE')))

            if not (criteria.get('NEWS_UUID') or criteria.get('NEWS_UUID_LIST')):
                group_by.append(orm_class.SORT_YEAR)
                with_entities.append(orm_class.SORT_YEAR)
                key.append('year')

                with_entities.append(func.count(orm_class.NEWS_COUNT).label('news_count'))
                order_by.append(text('news_count desc'))
                key.append('news_count')
                require_base = False

        if criteria.get('WEEK_DAY'):
            filter.append(orm_class.DAY_OF_WEEK == (criteria.get('WEEK_DAY')))
            group_by.append(orm_class.DAY_OF_WEEK)
            with_entities.append(orm_class.DAY_OF_WEEK)
            key.append('week_day')

        if criteria.get('YEAR'):
            group_by.append(orm_class.SORT_MONTH)
            with_entities.append(orm_class.SORT_MONTH)
            key.append('month')

        if criteria.get('MONTH'):
            if not criteria.get('WEEK_DAY'):
                group_by.append(orm_class.SORT_DAY)
                with_entities.append(orm_class.SORT_DAY)
                key.append('day')

        if criteria.get('DAY'):
            filter.append(orm_class.SORT_DAY == criteria.get('DAY'))

        if criteria.get('CATEGORY'):
            filter.append(orm_class.CATEGORY == criteria.get('CATEGORY'))

        if criteria.get('CATEGORY_LIST'):
            filter.append(orm_class.CATEGORY.in_(criteria.get('CATEGORY_LIST')))

        if require_base and (not (criteria.get('DATE') or criteria.get('DAY') or criteria.get('WEEK_DAY'))):
            group_by.append(orm_class.SORT_YEAR)
            with_entities.append(orm_class.SORT_YEAR)
            key.append('year')

            with_entities.append(func.count(orm_class.NEWS_COUNT).label('news_count'))
            order_by.append(text('news_count desc'))
            key.append('news_count')

        return { 'with_entities' : with_entities, 'filter' : filter, 'key' : key, 'order_by' : order_by, 'group_by' : group_by }

    def get_news_map_parameter (self, criteria, orm_class):
        with_entities = []
        filter = []
        key = []

        if criteria.get('NEWS_UUID'):
            filter.append(orm_class.NEWS_UUID.like(criteria.get('NEWS_UUID')))
            with_entities.append(orm_class.NEWS_UUID)
            with_entities.append(orm_class.NEWS_METADATA_KEY)
            with_entities.append(orm_class.NEWS_METADATA_VALUE)
            key.append('uuid')
            key.append('key')
            key.append('value')

        if criteria.get('DATE') or criteria.get('WEEK_DAY') or criteria.get('TAG') or criteria.get('SENTIMENT') or criteria.get('TOPIC'):
            with_entities.append(orm_class.NEWS_UUID)
            key.append('uuid')

        if criteria.get('DATE'):
            filter.append(orm_class.NEWS_DAY.like(criteria.get('DATE')))

        if criteria.get('WEEK_DAY'):
            filter.append(orm_class.DAY_OF_WEEK.like(criteria.get('WEEK_DAY')))

        if criteria.get('TAG'):
            filter.append(orm_class.NEWS_METADATA_KEY == 'tag')
            filter.append(orm_class.NEWS_METADATA_VALUE == criteria.get('CATEGORY'))

        if criteria.get('SENTIMENT'):
            filter.append(orm_class.NEWS_METADATA_KEY == 'sentiment')
            filter.append(orm_class.NEWS_METADATA_VALUE == criteria.get('SENTIMENT'))

        if criteria.get('TOPIC'):
            filter.append(orm_class.NEWS_METADATA_KEY == 'topic')
            filter.append(orm_class.NEWS_METADATA_VALUE == criteria.get('TOPIC'))

        if criteria.get('TAG_LIST'):
            filter.append(orm_class.NEWS_METADATA_KEY == 'tag')
            filter.append(orm_class.NEWS_METADATA_VALUE.in_(criteria.get('TAG_LIST')))

        if criteria.get('SENTIMENT_LIST'):
            filter.append(orm_class.NEWS_METADATA_KEY == 'sentiment')
            filter.append(orm_class.NEWS_METADATA_VALUE.in_(criteria.get('SENTIMENT_LIST')))

        if criteria.get('TOPIC_LIST'):
            filter.append(orm_class.NEWS_METADATA_KEY == 'topic')
            filter.append(orm_class.NEWS_METADATA_VALUE.in_(criteria.get('TOPIC_LIST')))

        return { 'with_entities' : with_entities, 'filter' : filter, 'key' : key }

    def get_metadata_parameter (self, criteria, orm_class, base_column, base_key):
        group_by = []
        with_entities = [ func.count(orm_class.NEWS_COUNT).label('news_count') ]
        filter = []
        order_by = [ text('news_count desc') ]
        key = [ 'news_count' ]
        require_base = True

        if criteria.get('DATE'):
            filter.append(orm_class.NEWS_DAY.like(criteria.get('DATE')))
            group_by.append(orm_class.SORT_YEAR)
            with_entities.append(orm_class.SORT_YEAR)
            key.append('year')

        if criteria.get('WEEK_DAY'):
            filter.append(orm_class.DAY_OF_WEEK == (criteria.get('WEEK_DAY')))
            group_by.append(orm_class.DAY_OF_WEEK)
            with_entities.append(orm_class.DAY_OF_WEEK)
            key.append('week_day')

        if criteria.get('YEAR'):
            group_by.append(orm_class.SORT_MONTH)
            with_entities.append(orm_class.SORT_MONTH)
            key.append('month')

        if criteria.get('MONTH'):
            if not criteria.get('WEEK_DAY'):
                group_by.append(orm_class.SORT_DAY)
                with_entities.append(orm_class.SORT_DAY)
                key.append('day')

        if criteria.get('DAY'):
            filter.append(orm_class.SORT_DAY == criteria.get('DAY'))

        if criteria.get('CATEGORY'):
            group_by.append(orm_class.CATEGORY)
            with_entities.append(orm_class.CATEGORY)
            filter.append(orm_class.CATEGORY == criteria.get('CATEGORY'))
            key.append('category')
            require_base = False

        if criteria.get('TAG'):
            group_by.append(orm_class.TAG)
            with_entities.append(orm_class.TAG)
            filter.append(orm_class.TAG == criteria.get('TAG'))
            key.append('tag')
            require_base = False

        if criteria.get('SENTIMENT'):
            group_by.append(orm_class.SENTIMENT)
            with_entities.append(orm_class.SENTIMENT)
            filter.append(orm_class.SENTIMENT == criteria.get('SENTIMENT'))
            key.append('sentiment')
            require_base = False

        if criteria.get('TOPIC'):
            group_by.append(orm_class.TOPIC)
            with_entities.append(orm_class.TOPIC)
            filter.append(orm_class.TOPIC == criteria.get('TOPIC'))
            key.append('topic')
            require_base = False

        if require_base and (not (criteria.get('DATE') or criteria.get('DAY') or criteria.get('WEEK_DAY'))):
            group_by.append(base_column)
            with_entities.append(base_column)
            key.append(base_key)

        if orm_class == AggregateCategory:
            group_by.append(base_column)
            with_entities.append(base_column)
            key.append(base_key)

        return { 'group_by' : group_by , 'with_entities' : with_entities, 'filter' : filter, 'key' : key, 'order_by' : order_by }