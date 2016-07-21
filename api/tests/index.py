import unittest
import json
import time
from datetime import datetime
from app import app
from app.views import index


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client and propagates the exceptions to the test
        client.
        '''
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_200(self):
        '''Tests that the status code response is is 200.'''
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

    def test_status(self):
        '''Tests that the response data "status" == "OK".'''
        res = self.app.get('/')
        d = json.loads(res.data)
        self.assertEqual(d.get("status"), "OK")

    def time_cmp(self, t_type, obj, el):
        '''Compares time up to the minute, raises an error if there is a
        difference.

        Keyword arguments:
        t_type -- The time type method of the datetime object (i.e., "now" for
        when using the method `datetime.now()`).
        obj -- The object to get the particular time string from.
        el -- The string element to compare. Must have data up to the sec.
        '''
        t_type = getattr(datetime, t_type)().strftime("%Y/%m/%d %H:%M")
        struct_time = time.strptime(obj.get(el), "%Y/%m/%d %H:%M:%S")
        self.assertEqual(t_type, time.strftime("%Y/%m/%d %H:%M", struct_time))

    def test_time(self):
        '''Tests that the response data status item is "time" is equal to the
        current time up to the minute.
        '''
        self.time_cmp("now", json.loads(self.app.get('/').data), "time")

    def test_time_utc(self):
        '''Tests that the response data status item is "utc_time" is equal to
        the current utc_time up to the minute.
        '''
        self.time_cmp("utcnow", json.loads(self.app.get('/').data), "utc_time")

if __name__ == '__main__':
    unittest.main()
