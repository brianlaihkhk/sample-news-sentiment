import unittest
import json
from misc import load_options
import sys
import os
import data

sys.path.append(os.path.abspath('../ETL'))
from etl.etl import Etl

class TestEtl(unittest.TestCase):
    etl_analysis = Etl('Sample/test.txt' , '20220222', data.sample_news, 'business')

    def test_data_extraction(self):
        self.assertEqual(self.etl_analysis.week_day , 'Tue')
        self.assertTrue(self.etl_analysis.title.split(' ')[0].lower() == 'ivanovic')
        self.assertEqual(self.etl_analysis.news_date , '20220222')
        self.assertEqual(self.etl_analysis.category , 'business')

    def test_sentiment_extraction(self):
        self.assertTrue(len(self.etl_analysis.sentiment) > 0)
        self.assertTrue(len(self.etl_analysis.topic) > 0)
        self.assertTrue(len(self.etl_analysis.tags) > 0)

if __name__ == "__main__":
    load_options("../ETL/.env.dev", 'file')
    unittest.main()