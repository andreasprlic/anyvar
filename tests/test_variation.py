from webtest import TestApp
import unittest
import json
from anyvar import run
from parameterized import parameterized
import os

base_url = "/variation"

content_type = "application/json"

base_test_data_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
)
file_object = os.path.join(base_test_data_dir, "alleles.json")
with open(file_object) as f:
    tests = json.load(f)


class TestVariation(unittest.TestCase):
    # could also be set up globally outside of this class
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp(run(actually_run=False))

    @parameterized.expand(tests.keys())
    def test_00_put(self, id):
        # we need to first create the allele before the next couple of tests can work with it.
        params = json.dumps(tests[id]["params"])
        response = self.app.put("/allele", params=params, content_type=content_type)
        assert response.status_code == 200

        self.assertDictEqual(response.json, tests[id]["response"])

    @parameterized.expand(tests.keys())
    def test_10_get(self, id):
        response = self.app.get(base_url + "/" + id)
        assert response.status_code == 200

        self.assertDictEqual(response.json, tests[id]["response"]["object"])
