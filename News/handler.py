from query import Query
from interaction import Interaction
from urllib.parse import urlparse
import logging
import os

class Handler():

    def __init__(self, db):
        self.application_prefix = os.environ['APPLICATION_PREFIX']
        self.query = Query(db)
        self.interaction = Interaction(db)

    def handle_search (self, query_string):
        query = {}
        print(query_string)
        query_components = dict(qc.split("=") for qc in query_string.split("&"))
        if query_components.get("date"):
            query.update(self.handle_date(query_components["date"]))
        if query_components.get("category"):
            query.update({'CATEGORY_LIST' : query_components["category"].split(',') })
        if query_components.get("tag"):
            query.update({'TAG_LIST' : query_components["tag"].split(',') })
        if query_components.get("sentiment"):
            query.update({'SENTIMENT_LIST' : query_components["sentiment"].split(',') })
        if query_components.get("topic"):
            query.update({'TOPIC_LIST' : query_components["topic"].split(',') })
        return query

    def handle_date(self, day_string):
        filter = {}
        week_data = day_string.split('-')

        if len(week_data) == 4 and str(week_data[0]):
            filter['WEEK_DAY'] = week_data[0]

        if len(week_data) == 4 and str(week_data[3]) and str(week_data[2]) and str(week_data[1]):
            filter['DATE'] = str(week_data[1]) + str(week_data[2]) + str(week_data[3])
            filter['YEAR'] = str(week_data[1])
            filter['MONTH'] = str(week_data[2])
            filter['DAY'] = str(week_data[3])
        elif len(week_data) == 4 and str(week_data[2]) and str(week_data[1]):
            filter['DATE'] = str(week_data[1]) + str(week_data[2]) + "%"
            filter['YEAR'] = str(week_data[1])
            filter['MONTH'] = str(week_data[2])
        elif len(week_data) == 4 and str(week_data[1]):
            filter['DATE'] = str(week_data[1]) + "%"
            filter['YEAR'] = str(week_data[1])
        elif len(week_data) == 4 and not str(week_data[3]) and not str(week_data[2]) and not str(week_data[1]) :
            filter['DATE'] = "%"
        else :
            raise Exception('Unsupported date query format')

        return filter

    def handle_query(self, date, value, key):
        if date and value:
            query = {key : value}
            query.update(self.handle_date(date))
            print(query)
        elif date:
            query = {}
            query.update(self.handle_date(date))
        elif not (date and value):
            query = {}
        else :
            raise Exception('Unsupported query_path query format')
        return query 

    def handle_news(self, category, uuid):
        query = {}
        if category and uuid:
            query = {'CATEGORY' : category, 'NEWS_UUID' : uuid}
        elif category:
            query = {'CATEGORY' : category}
        return query

    def handle_rating(self, uuid, rating):
        self.interaction.add_news_rating(uuid, rating)