from etl import Etl, Aggregate
from orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, News, NewsMap
import yaml
import datetime
import random
import uuid
from misc import load_env
import sys
from db import Database
import os

db_connection = None

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

class FileContext:
    def __init__(self, path, category):
        self.path = path
        self.scanned = './scanned.txt'
        self.category = category

    def process(self):
        file_list = list(set(self.get_file_list(self.path)) - set(self.get_scanned_file(self.scanned)))
        for context in file_list :
            # context_list = [ Etl(self.get_random_date(), self.get_context(context), self.category) for context in file_list ]
            context_list = [ Etl(self.get_random_date(), self.get_context(context), self.category) ]
            aggregates = Aggregate(context_list)
            self.process_news(context_list)
            self.process_aggregate_category(aggregates.aggregate_category)
            self.process_aggregate_sentiment(aggregates.aggregate_sentiment)
            self.process_aggregate_topic(aggregates.aggregate_topic)
            self.process_aggregate_tags(aggregates.aggregate_tags)
            self.save_scanned_file(self.scanned, file_list)

    def get_context(self, path):
        lines = ['', '']
        with open(path) as f:
            try:
                lines = f.readlines()
            except Exception as exc:
                print(exc)
                raise Exception('Unable to load file')
        return lines

    def get_scanned_file(self, file):
        file_list = []
        with open(file) as f:
            try:
                file_list = yaml.safe_load(f)
                if file_list is None:
                    file_list = []
            except yaml.YAMLError as exc:
                print(exc)
                raise Exception('Unable to open scanned list')
        return file_list

    def save_scanned_file(self, file, context):
        try:
            file = open(file, 'a', buffering=1)
            file.write(yaml.dump(context, file, Dumper=NoAliasDumper))
            file.close()
        except Exception as exc:
            print(exc)
            raise Exception('Unable to save scanned list')
        return True

    def get_file_list(self, path):
        file_list = []
        for file in os.listdir(path):
            if file.endswith(".txt"):
                file_list.append(os.path.join(path, file))
        return file_list

    def get_random_date(self):
        start_date = datetime.date(2020, 1, 1)
        end_date = datetime.date(2020, 2, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return random_date.strftime('%Y%m%d')

    def process_aggregate_category(self, aggregate_category):
        for key in aggregate_category:
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'CATEGORY': key[2] }
            result = AggregateCategory.query.filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateCategory(key[0], key[1], key[2], aggregate_category[key]))
            else :
                result.NEWS_COUNT += aggregate_category[key]
            db_connection.session.commit()
        
    def process_aggregate_sentiment(self, aggregate_sentiment):
        for key in aggregate_sentiment:
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'SENTIMENT': key[2] }
            result = AggregateSentiment.query.filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateSentiment(key[0], key[1], key[2], aggregate_sentiment[key]))
            else :
                result.NEWS_COUNT += aggregate_sentiment[key]
            db_connection.session.commit()

    def process_aggregate_topic(self, aggregate_topic):
        for key in aggregate_topic:
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'TOPIC': key[2] }
            result = AggregateTopic.query.filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateTopic(key[0], key[1], key[2], aggregate_topic[key]))
            else :
                result.NEWS_COUNT += aggregate_topic[key]
            db_connection.session.commit()

    def process_aggregate_tags(self, aggregate_tags):
        for key in aggregate_tags:
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'TAG': key[2] }
            result = AggregateTag.query.filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateTag(key[0], key[1], key[2], aggregate_tags[key]))
            else :
                result.NEWS_COUNT += aggregate_tags[key]
            db_connection.session.commit()

    def process_news(self, news_list):
        for news in news_list:
            news_uuid = str(uuid.uuid4())
            db_connection.session.add(News(news_uuid, news.news_date, news.title, news.context))
            db_connection.session.add(NewsMap(news_uuid, 'sentiment', news.sentiment))
            db_connection.session.add(NewsMap(news_uuid, 'category', news.category))
            for topic in news.topic:
                db_connection.session.add(NewsMap(news_uuid, 'topic', topic))
            for tag in news.tags:
                db_connection.session.add(NewsMap(news_uuid, 'tag', tag))
            db_connection.session.commit()




if __name__ == "__main__":
    load_env(sys.argv[1])
    db_connection = Database().db
    FileContext("../Sample/bbc/business", 'business').process()
    FileContext("../Sample/bbc/entertainment", 'entertainment').process()
    FileContext("../Sample/bbc/politics", 'politics').process()
    FileContext("../Sample/bbc/sport", 'sport').process()
    FileContext("../Sample/bbc/tech", 'tech').process()