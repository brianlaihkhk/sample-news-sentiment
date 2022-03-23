import unittest
import yaml
import json
from misc import load_env

class TestEtl(unittest.TestCase):
    event = {}
    context = {}

    def test_get_item(self):
        response = json.loads(list(self.event, self.context)["body"])
        self.assertEqual(True, response["success"])


if __name__ == "__main__":
    load_env("../ETL/.env.dev")
    unittest.main()