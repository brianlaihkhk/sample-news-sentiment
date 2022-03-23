import unittest
import json
from misc import load_env

class TestNews(unittest.TestCase):
    event = {}
    context = {}

    def test_get_item(self):
        response = json.loads(list(self.event, self.context)["body"])
        self.assertEqual(True, response["success"])


if __name__ == "__main__":
    load_env("../News/.env.dev")
    unittest.main()