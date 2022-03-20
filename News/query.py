import response
from orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, AggregateInteraction, News, NewsMap
from db import Database
from sqlalchemy import or_, and_

class Query:
    def __init__(self):
        self.db_connection = Database().db
        self.query_limit = 50

    def get_news(self, event) :
        result = {}

        result_news = self.db_connection.session.query(News).with_entities(News.NEWS_UUID, News.NEWS_DAY, News.NEWS_TITLE, News.NEWS_CONTEXT, News.CATEGORY, News.RATING).filter_by(**event.get('query')).limit(self.query_limit).all()
        result['news'] = [{'uuid' : uuid, 'news_day' : news_day, 'news_title' : news_title, 'news_content' : news_content, 'category' : category, 'rating' : rating} for uuid, news_day, news_title, news_content, category, rating in result_news]

        if len(result_news) == 1 and (event.get('query').get('NEWS_UUID') is not None) :
            result_metadata = self.db_connection.session.query(NewsMap).with_entities(NewsMap.NEWS_METADATA_KEY, NewsMap.NEWS_METADATA_VALUE).filter_by({'NEWS_UUID' : event.get('query').get('NEWS_UUID')}).all()

            result['metadata'] = [{'news_metadata_key' : news_metadata_key, 'news_metadata_value' : news_metadata_value} for news_metadata_key, news_metadata_value in result_metadata]

            self.update_news_count(result_news[0])
            self.update_category_count(self.get_category({'query' : {'CATEGORY' : result_news[0].CATEGORY, 'NEWS_DAY' : result_news[0].NEWS_DAY}}))

            # for news_metadata_key, news_metadata_value in result_metadata:
            #     if news_metadata_key == 'topic':
            #         self.update_topic_count(self.get_category({'query' : {'TOPIC' : news_metadata_value, 'NEWS_DAY' : result_news[0].NEWS_DAY}}))
            #     elif news_metadata_key == 'sentiment':
            #         self.update_sentiment_count(self.get_category({'query' : {'SENTIMENT' : news_metadata_value, 'NEWS_DAY' : result_news[0].NEWS_DAY}}))
            #     elif news_metadata_key == 'tag':
            #         self.update_tag_count(self.get_category({'query' : {'TAG' : news_metadata_value, 'NEWS_DAY' : result_news[0].NEWS_DAY}}))

        return response.success(result)

    def update_news_count(self, news):
        news.POPULARITY += 1
        self.db_connection.session.commit()

    def update_category_count(self, category_list):
        for category in category_list:
            category.POPULARITY += 1
        self.db_connection.session.commit()

    def get_category(self, event) :
        print(event.get('query').get('DATE'))
        print(event.get('query').get('WEEK_DAY'))

        category_filter = and_(AggregateCategory.CATEGORY.like(event.get('query').get('CATEGORY')), AggregateCategory.NEWS_DAY.like(event.get('query').get('DATE')), AggregateCategory.DAY_OF_WEEK.like(event.get('query').get('WEEK_DAY')))

        category_result = self.db_connection.session.query(AggregateCategory).filter(category_filter).order_by(AggregateCategory.POPULARITY.desc()).limit(self.query_limit).all()

        self.update_category_count(category_result)

        result = [{'news_day' : row.NEWS_DAY, 'day_of_week' : row.DAY_OF_WEEK, 'category': row.CATEGORY, 'news_count' : row.NEWS_COUNT, 'popularity' : row.POPULARITY} for row in category_result]

        return result

    def update_topic_count(self, topic_list):
        for topic in topic_list:
            topic.POPULARITY += 1
        self.db_connection.session.commit()


    def get_topic(self, event) :
        topic_filter = and_(AggregateTopic.TOPIC.like(event.get('query').get('TOPIC')), AggregateTopic.NEWS_DAY.like(event.get('query').get('DATE')), AggregateTopic.DAY_OF_WEEK.like(event.get('query').get('WEEK_DAY')))

        topic_result = self.db_connection.session.query(AggregateTopic).filter(topic_filter).order_by(AggregateTopic.POPULARITY.desc()).limit(self.query_limit).all()

        self.update_topic_count(topic_result)

        result = [{'news_day' : row.NEWS_DAY, 'day_of_week' : row.DAY_OF_WEEK, 'topic': row.TOPIC, 'news_count' : row.NEWS_COUNT, 'popularity' : row.POPULARITY} for row in topic_result]

        return result


    def update_tag_count(self, tag_list):
        for tag in tag_list:
            tag.POPULARITY += 1
        self.db_connection.session.commit()

    def get_tag(self, event) :
        tag_filter = and_(AggregateTag.TAG.like(event.get('query').get('TAG')), AggregateTag.NEWS_DAY.like(event.get('query').get('DATE')), AggregateTag.DAY_OF_WEEK.like(event.get('query').get('WEEK_DAY')))

        tag_result = self.db_connection.session.query(AggregateTag).filter(tag_filter).order_by(AggregateTag.POPULARITY.desc()).limit(self.query_limit).all()

        self.update_tag_count(tag_result)

        result = [{'news_day' : row.NEWS_DAY, 'day_of_week' : row.DAY_OF_WEEK, 'tag': row.TAG, 'news_count' : row.NEWS_COUNT, 'popularity' : row.POPULARITY} for row in tag_result]

        return result


    def update_sentiment_count(self, sentiment_list):
        for sentiment in sentiment_list:
            sentiment.POPULARITY += 1
        self.db_connection.session.commit()

    def get_sentiment(self, event) :
        topic_filter = and_(AggregateSentiment.SENTIMENT.like(event.get('query').get('SENTIMENT')), AggregateSentiment.NEWS_DAY.like(event.get('query').get('DATE')), AggregateSentiment.DAY_OF_WEEK.like(event.get('query').get('WEEK_DAY')))

        sentiment_result = self.db_connection.session.query(AggregateSentiment).filter(topic_filter).order_by(AggregateSentiment.POPULARITY.desc()).limit(self.query_limit).all()

        self.update_sentiment_count(sentiment_result)

        result = [{'news_day' : row.NEWS_DAY, 'day_of_week' : row.DAY_OF_WEEK, 'sentiment': row.SENTIMENT, 'news_count' : row.NEWS_COUNT, 'popularity' : row.POPULARITY} for row in sentiment_result]

        return result