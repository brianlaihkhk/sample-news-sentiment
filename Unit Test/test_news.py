import unittest
import json
from misc import load_options
import sys
import os
import data

sys.path.append(os.path.abspath('../News'))
from handler import Handler
from orm import AggregateCategory, AggregateSentiment, AggregateTopic, AggregateTag, News, NewsMap

class TestNews(unittest.TestCase):
    handler = Handler(None)
    query = handler.query


    def test_handle_search(self):
        criteria_1 = self.handler.handle_search(data.url_query_string_1)
        criteria_2 = self.handler.handle_search(data.url_query_string_2)
        criteria_3 = self.handler.handle_search(data.url_query_string_3)

        self.assertTrue('CATEGORY_LIST' in criteria_1 and len(criteria_1['CATEGORY_LIST']) == 3)
        self.assertTrue('DATE' in criteria_1 and criteria_1['DATE'] == '202008%')
        self.assertTrue('TAG_LIST' in criteria_2 and len(criteria_2['TAG_LIST']) == 3)
        self.assertTrue('CATEGORY_LIST' in criteria_2 and criteria_2['CATEGORY_LIST'][0] == 'sport')
        self.assertTrue('SENTIMENT_LIST' in criteria_2 and criteria_2['SENTIMENT_LIST'][0] == 'pos')
        self.assertTrue('TOPIC_LIST' in criteria_3 and criteria_3['TOPIC_LIST'][0] == 'money')
        self.assertTrue('WEEK_DAY' in criteria_3 and criteria_3['WEEK_DAY'] == 'Wed')

    def test_handle_news_stat(self):
        criteria_1 = self.handler.handle_news_stat(None, None)
        criteria_2 = self.handler.handle_news_stat('-2020--', None)
        criteria_3 = self.handler.handle_news_stat('Wed---', None)
        criteria_4 = self.handler.handle_news_stat('Wed-2020--', None)
        criteria_5 = self.handler.handle_news_stat('Wed-2020--', 'business')
        criteria_6 = self.handler.handle_news_stat('---', None)

        self.assertTrue('DATE' not in criteria_1 and 'CATEGORY' not in criteria_1)

        self.assertTrue('DATE' in criteria_2 and 'CATEGORY' not in criteria_2)
        self.assertTrue(criteria_2['DATE'] == '2020%')

        self.assertTrue('DATE' in criteria_3 and 'YEAR' not in criteria_3)
        self.assertTrue(criteria_3['WEEK_DAY'] == 'Wed')

        self.assertTrue('DATE' in criteria_4 and 'YEAR' in criteria_4)
        self.assertTrue(criteria_4['WEEK_DAY'] == 'Wed')
        self.assertTrue(criteria_4['YEAR'] == '2020')
        self.assertTrue(criteria_4['DATE'] == '2020%')

        self.assertTrue('CATEGORY' in criteria_5)
        self.assertTrue(criteria_5['CATEGORY'] == 'business')

        self.assertTrue('DATE' in criteria_6)
        self.assertTrue(criteria_6['DATE'] == '%')

    def test_handle_news(self):
        criteria_1 = self.handler.handle_news(None, None)
        criteria_2 = self.handler.handle_news('business', None)
        criteria_3 = self.handler.handle_news('tech', 'f7f8f4dc-5fb7-491c-8e05-df278d0b5bd7')

        self.assertTrue('CATEGORY' not in criteria_1 and 'NEWS_UUID' not in criteria_1)

        self.assertTrue('CATEGORY' in criteria_2 and 'NEWS_UUID' not in criteria_2)
        self.assertTrue(criteria_2['CATEGORY'] == 'business')

        self.assertTrue('CATEGORY' in criteria_3 and 'NEWS_UUID' in criteria_3)
        self.assertTrue(criteria_3['CATEGORY'] == 'tech')
        self.assertTrue(criteria_3['NEWS_UUID'] == 'f7f8f4dc-5fb7-491c-8e05-df278d0b5bd7')

    def test_handle_query(self):
        criteria_1 = self.handler.handle_query(None, None, 'CATEGORY')
        criteria_2 = self.handler.handle_query('---', None, 'TOPIC')
        criteria_3 = self.handler.handle_query('Thu-2020-08-04', 'pos', 'SENTIMENT')

        self.assertTrue('CATEGORY' not in criteria_1 and 'DATE' not in criteria_1)

        self.assertTrue('TOPIC' not in criteria_2 and 'DATE' in criteria_2)
        self.assertTrue(criteria_2['DATE'] == '%')

        self.assertTrue('SENTIMENT' in criteria_3 and 'DATE' in criteria_3)
        self.assertTrue('WEEK_DAY' in criteria_3)
        self.assertTrue('YEAR' in criteria_3)
        self.assertTrue('MONTH' in criteria_3)
        self.assertTrue('DAY' in criteria_3)
        self.assertTrue(criteria_3['DATE'] == '20200804')
        self.assertTrue(criteria_3['YEAR'] == '2020')
        self.assertTrue(criteria_3['MONTH'] == '08')
        self.assertTrue(criteria_3['DAY'] == '04')
        self.assertTrue(criteria_3['SENTIMENT'] == 'pos')

    def test_handle_date(self):
        criteria_1 = self.handler.handle_date('---')
        criteria_2 = self.handler.handle_date('Fri-2021-08-12')

        self.assertRaises(Exception, self.test_handle_date, '-') 
        self.assertRaises(Exception, self.test_handle_date, 'Fri--02-15')
        self.assertRaises(Exception, self.test_handle_date, '--02-15')
        self.assertRaises(Exception, self.test_handle_date, '---15')
        self.assertRaises(Exception, self.test_handle_date, '-2020--15')
        self.assertRaises(Exception, self.test_handle_date, 'Fri---15')

        self.assertTrue('DATE' in criteria_1)
        self.assertTrue(criteria_1['DATE'] == '%')

        self.assertTrue('DATE' in criteria_2 and criteria_2['DATE'] == '20210812')
        self.assertTrue('YEAR' in criteria_2 and criteria_2['YEAR'] == '2021')
        self.assertTrue('MONTH' in criteria_2 and criteria_2['MONTH'] == '08')
        self.assertTrue('DAY' in criteria_2 and criteria_2['DAY'] == '12')


    def test_get_news_parameter(self):
        criteria_1 = self.handler.handle_news('tech', 'f7f8f4dc-5fb7-491c-8e05-df278d0b5bd7')
        query_parameter_1 = self.query.get_news_parameter(criteria_1, News)

        criteria_2 = self.handler.handle_query('-2020--', None, 'CATEGORY')
        query_parameter_2 = self.query.get_news_parameter(criteria_2, News)

        # filter : Category + UUID
        self.assertTrue(len(query_parameter_1['filter']) == 2)
        # with_entities : output fields in news
        self.assertTrue(len(query_parameter_1['with_entities']) >= 6)
        # no order by and group by
        self.assertTrue(len(query_parameter_1['order_by']) == 0)
        self.assertTrue(len(query_parameter_1['group_by']) == 0)

        # filter : filter by year
        self.assertTrue(len(query_parameter_2['filter']) >= 1)
        # with_entities : must have news_count and year field
        self.assertTrue(len(query_parameter_2['with_entities']) >= 2)
        # order by total news count and group by year
        self.assertTrue(len(query_parameter_2['order_by']) == 1)
        self.assertTrue(len(query_parameter_2['group_by']) >= 1)


    def test_get_news_map_parameter(self):
        criteria_1 = {'NEWS_UUID' : '8e90b5b4-fb51-46ef-897a-e7b93b11b34e', 'TOPIC': 'money'}
        query_parameter_1 = self.query.get_news_map_parameter(criteria_1, NewsMap)

        criteria_2 = {'NEWS_UUID' : '8e90b5b4-fb51-46ef-897a-e7b93b11b34e'}
        query_parameter_2 = self.query.get_news_map_parameter(criteria_2, NewsMap)

        # filter : topic amd news_uuid filter
        self.assertTrue(len(query_parameter_1['filter']) == 2)
        # with_entities : select news_count, key, value
        self.assertTrue(len(query_parameter_1['with_entities']) >= 3)

        # filter : news_uuid
        self.assertTrue(len(query_parameter_2['filter']) == 1)
        # with_entities : output news_uuid , meta key and meta value
        self.assertTrue(len(query_parameter_2['with_entities']) >= 3)


    def test_get_metadata_parameter(self):
        criteria_1 = {"SENTIMENT" : "pos"}
        query_parameter_1 = self.query.get_metadata_parameter(criteria_1, AggregateSentiment, AggregateSentiment.SENTIMENT, 'sentiment')

        # filter : Filter 
        self.assertTrue(len(query_parameter_1['filter']) >= 1)
        # with_entities : select news_count, sentiment
        self.assertTrue(len(query_parameter_1['with_entities']) >= 2)
        # order by news count, group by sentiment
        self.assertTrue(len(query_parameter_1['order_by']) == 1)
        self.assertTrue(len(query_parameter_1['group_by']) == 1)

if __name__ == "__main__":
    load_options("../News/.env.dev", 'file')
    unittest.main()