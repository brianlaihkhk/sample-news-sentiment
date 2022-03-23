import unittest
import json
from misc import load_options
import sys
import os
import data

sys.path.append(os.path.abspath('../ETL'))
from etl.etl import Etl

class TestEtl(unittest.TestCase):

    def __init__(self):
        self.etl_analysis = Etl('Sample/test.txt' , '20220222', data.sample_news, 'business')

    def test(self):



if __name__ == "__main__":
    load_options("../ETL/.env.dev")
    unittest.main()