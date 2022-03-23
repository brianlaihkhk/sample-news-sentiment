from etl.analysis import Analysis
import time
import re

regex = '[^a-zA-Z \n\.]'

class Etl:
    def __init__(self, news_path, news_date, context, category):
        self.path = news_path
        self.title = re.sub(regex, '', context[0]).strip()
        self.news_date = news_date
        self.week_day = time.strftime("%a", time.strptime(self.news_date, "%Y%m%d"))
        self.context = re.sub(regex, '', ''.join(context[1:])).strip()
        self.analysis = Analysis(self.context, category)
        self.sentiment = self.analysis.sentiment
        self.topic = self.analysis.topic
        self.category = category
        self.tags = self.analysis.tags

class Aggregate:
    def __init__(self, etl_list):
        self.category = self.aggregate_category(etl_list)
        self.sentiment = self.aggregate_sentiment(etl_list)
        self.topic = self.aggregate_topic(etl_list)
        self.tags = self.aggregate_tags(etl_list)

    def aggregate_category (self, etl_list):
        aggregate_category_list = {}
        for etl in etl_list:
            key = (etl.news_date, etl.week_day, etl.category)
            if (aggregate_category_list.get(key) == None):
                aggregate_category_list[key] = 1
            else :
                aggregate_category_list[key] += 1
        return aggregate_category_list

    def aggregate_sentiment (self, etl_list):
        aggregate_sentiment_list = {}
        for etl in etl_list:
            key = (etl.news_date, etl.week_day, etl.sentiment)
            if (aggregate_sentiment_list.get(key) == None):
                aggregate_sentiment_list[key] = 1
            else :
                aggregate_sentiment_list[key] += 1
        return aggregate_sentiment_list

    def aggregate_topic (self, etl_list):
        aggregate_topic_list = {}
        for etl in etl_list:
            for topic in etl.topic:
                key = (etl.news_date, etl.week_day, topic)
                if (aggregate_topic_list.get(key) == None):
                    aggregate_topic_list[key] = 1
                else :
                    aggregate_topic_list[key] += 1
        return aggregate_topic_list

    def aggregate_tags (self, etl_list):
        aggregate_tag_list = {}
        for etl in etl_list:
            for tag in etl.tags:
                key = (etl.news_date, etl.week_day, tag)
                if (aggregate_tag_list.get(key) == None):
                    aggregate_tag_list[key] = 1
                else :
                    aggregate_tag_list[key] += 1
        return aggregate_tag_list
        
