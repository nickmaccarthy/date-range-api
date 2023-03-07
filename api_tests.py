import vcr
import requests
import json 
import unittest
from pprint import pprint
from os import environ as env

class TestDateRangeAPI(unittest.TestCase):
    BASE_URL = env.get('BASE_URL', 'http://localhost:5001')

    @vcr.use_cassette()
    def test_range_overlap_true(self):
        # with just dates, ie YYYY-MM-DD
        response = requests.get(f'{self.BASE_URL}/?range1=2023-01-01,2023-01-05&range2=2023-01-01,2023-01-04')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response._content)
        self.assertTrue(json_response.get('ranges_overlap'))
        self.assertEqual(json_response['range1']['start'], '2023-01-01')

        # test with timeformats with minutes like YYYY-MM-DDTHH:mm:ss
        response = requests.get(f'{self.BASE_URL}/?range1=2023-01-01T00:00:00,2023-01-01T00:01:00&range2=2023-01-01T00:00:00,2023-01-01T00:00:30')
        json_response = json.loads(response._content)
        self.assertTrue(json_response.get('ranges_overlap'))

    @vcr.use_cassette()
    def test_range_overlap_datemath(self):
        # test with datemath to test the python-datemath module more
        response = requests.get(f'{self.BASE_URL}/?range1=now-1h,now&range2=now-30m,now')
        json_response = json.loads(response._content)
        self.assertTrue(json_response.get('ranges_overlap'))

    @vcr.use_cassette()
    def test_ranges_dont_overlap(self):
        response = requests.get(f'{self.BASE_URL}/?range1=2021-01-01,2021-01-05&range2=2023-01-01,2023-01-04')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response._content)
        self.assertFalse(json_response.get('ranges_overlap'))
        self.assertEqual(json_response['range1']['start'], '2021-01-01')

    @vcr.use_cassette()
    def test_invalid_date_fomat(self):
        response = requests.get(f'{self.BASE_URL}/?range1=GARBAGE_DATE_FORMAT1,ANOTHER_ONE&range2=2023-01-01,2023-01-04')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid time component provided.', response._content)

    @vcr.use_cassette()
    def test_failure_on_post_request(self):
        response = requests.post(f'{self.BASE_URL}/?range1=2023-01-01T00:00:00,2023-01-01T00:01:00&range2=2023-01-01T00:00:00,2023-01-01T00:00:30')
        self.assertEqual(response.status_code, 405)
