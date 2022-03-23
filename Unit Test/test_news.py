import unittest
import json
from misc import load_options
import sys
import os

sys.path.append(os.path.abspath('../News'))

class TestNews(unittest.TestCase):
    event = {}
    context = {}

    def test_get_item(self):
        response = json.loads(list(self.event, self.context)["body"])
        self.assertEqual(True, response["success"])


if __name__ == "__main__":
    load_options("../News/.env.dev")
    unittest.main()