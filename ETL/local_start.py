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
            context_list = [ Etl(context, self.get_random_date(), self.get_context(context), self.category) ]
            aggregates = Aggregate(context_list)
            self.process_news(context_list)
            self.process_aggregate_category(aggregates.aggregate_category(context_list))
            self.process_aggregate_sentiment(aggregates.aggregate_sentiment(context_list))
            self.process_aggregate_topic(aggregates.aggregate_topic(context_list))
            self.process_aggregate_tags(aggregates.aggregate_tags(context_list))
            self.save_scanned_file(self.scanned, [ context ])

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
        print(context)
        if context != None and len(context) > 0 :
            try:
                file = open(file, 'a', buffering=1)
                yaml.dump(context, file, Dumper=NoAliasDumper)
                file.close()
            except Exception as exc:
                print(exc)
                raise Exception('Unable to save scanned list')
        else:
            return False
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
        for key in aggregate_category.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'CATEGORY': key[2] }
            result = db_connection.session.query(AggregateCategory).filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateCategory(key[0], key[1], key[2], aggregate_category[key]))

            else :
                result.NEWS_COUNT += aggregate_category[key]
            print('aggregate_category : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_category[key]))

            db_connection.session.commit()
        
    def process_aggregate_sentiment(self, aggregate_sentiment):
        for key in aggregate_sentiment.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'SENTIMENT': key[2] }
            result = db_connection.session.query(AggregateSentiment).filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateSentiment(key[0], key[1], key[2], aggregate_sentiment[key]))

            else :
                result.NEWS_COUNT += aggregate_sentiment[key]
            print('aggregate_sentiment : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_sentiment[key]))

            db_connection.session.commit()

    def process_aggregate_topic(self, aggregate_topic):
        for key in aggregate_topic.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'TOPIC': key[2] }
            result = db_connection.session.query(AggregateTopic).filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateTopic(key[0], key[1], key[2], aggregate_topic[key]))
            else :
                result.NEWS_COUNT += aggregate_topic[key]
            print('aggregate_topic : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_topic[key]))

            db_connection.session.commit()

    def process_aggregate_tags(self, aggregate_tags):
        for key in aggregate_tags.keys():
            filters = {'NEWS_DAY': key[0], 'DAY_OF_WEEK': key[1], 'TAG': key[2] }
            result = db_connection.session.query(AggregateTag).filter_by(**filters).first()

            if result is None:
                db_connection.session.add(AggregateTag(key[0], key[1], key[2], aggregate_tags[key]))
            else :
                result.NEWS_COUNT += aggregate_tags[key]
            print('aggregate_tags : ' + key[0] + ' ' + key[1] + ' ' + key[2] + ' ' + str(aggregate_tags[key]))

            db_connection.session.commit()

    def process_news(self, news_list):
        for news in news_list:
            try :
                news_uuid = str(uuid.uuid4())
                db_connection.session.add(News(news_uuid, news.news_date, news.title, news.context))
                db_connection.session.commit()

                db_connection.session.add(NewsMap(news_uuid, 'sentiment', news.sentiment))
                db_connection.session.commit()

                db_connection.session.add(NewsMap(news_uuid, 'category', news.category))
                db_connection.session.commit()

                print('news_date : ' + news.news_date)
                print('title : ' + news.title)
                print('sentiment : ' + news.sentiment)
                print('category : ' + news.category)

                for topic in news.topic:
                    print('topic : ' + str(topic))
                    db_connection.session.add(NewsMap(news_uuid, 'topic', topic))
                    db_connection.session.commit()
                for tag in news.tags:
                    print('tag : ' + tag)
                    db_connection.session.add(NewsMap(news_uuid, 'tag', tag))
                    db_connection.session.commit()
            except Exception as e:
                print(e)
                raise Exception('Unable to process file : ' + news.path)





if __name__ == "__main__":
    load_env(sys.argv[1])
    db_connection = Database().db
    FileContext("../Sample/bbc/business", 'business').process()
    FileContext("../Sample/bbc/entertainment", 'entertainment').process()
    FileContext("../Sample/bbc/politics", 'politics').process()
    FileContext("../Sample/bbc/sport", 'sport').process()
    FileContext("../Sample/bbc/tech", 'tech').process()