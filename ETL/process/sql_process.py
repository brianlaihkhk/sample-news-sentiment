from process.orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, News, NewsMap
import datetime
import random
import uuid
from process.db import Database
import logging


class SqlProcess:

    def __init__(self, path, category):
        self.path = path
        self.category = category
        self.db_connection = Database().db

    def get_random_date(self):
        start_date = datetime.date(2018, 1, 1)
        end_date = datetime.date(2021, 12, 31)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return random_date.strftime('%Y%m%d')

    def process_aggregate_category(self, aggregate_category):
        for key in aggregate_category.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'CATEGORY': key[2] }
            result = self.db_connection.session.query(AggregateCategory).filter_by(**filters).first()

            if result is None:
                self.db_connection.session.add(AggregateCategory(key[0], key[1], key[2], aggregate_category[key]))

            else :
                result.NEWS_COUNT += aggregate_category[key]
            logging.info('aggregate_category : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_category[key]))
        
    def process_aggregate_sentiment(self, aggregate_sentiment):
        for key in aggregate_sentiment.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'SENTIMENT': key[2] }
            result = self.db_connection.session.query(AggregateSentiment).filter_by(**filters).first()

            if result is None:
                self.db_connection.session.add(AggregateSentiment(key[0], key[1], key[2], aggregate_sentiment[key]))

            else :
                result.NEWS_COUNT += aggregate_sentiment[key]
            logging.info('aggregate_sentiment : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_sentiment[key]))

    def process_aggregate_topic(self, aggregate_topic):
        for key in aggregate_topic.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'TOPIC': key[2] }
            result = self.db_connection.session.query(AggregateTopic).filter_by(**filters).first()

            if result is None:
                self.db_connection.session.add(AggregateTopic(key[0], key[1], key[2], aggregate_topic[key]))
            else :
                result.NEWS_COUNT += aggregate_topic[key]
            logging.info('aggregate_topic : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_topic[key]))

    def process_aggregate_tags(self, aggregate_tags):
        for key in aggregate_tags.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'TAG': key[2] }
            result = self.db_connection.session.query(AggregateTag).filter_by(**filters).first()

            if result is None:
                self.db_connection.session.add(AggregateTag(key[0], key[1], key[2], aggregate_tags[key]))
            else :
                result.NEWS_COUNT += aggregate_tags[key]
            logging.info('aggregate_tags : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_tags[key]))

    def process_news(self, news_list):
        for news in news_list:
            try :
                news_uuid = str(uuid.uuid4())
                self.db_connection.session.add(News(news_uuid, news.news_date, news.week_day, news.title, news.context, news.category))
                self.db_connection.session.commit()
                self.db_connection.session.add(NewsMap(news_uuid, news.news_date, news.week_day, 'sentiment', news.sentiment))
                self.db_connection.session.commit()

                for topic in news.topic:
                    logging.info('topic : ' + str(topic))
                    self.db_connection.session.add(NewsMap(news_uuid, news.news_date, news.week_day, 'topic', topic))
                    self.db_connection.session.commit()
                for tag in news.tags:
                    logging.info('tag : ' + tag)
                    self.db_connection.session.add(NewsMap(news_uuid, news.news_date, news.week_day, 'tag', tag))
                    self.db_connection.session.commit()
            except Exception as e:
                logging.error(str(e))
                raise Exception('Unable to process file : ' + news.path)