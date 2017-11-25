
import unittest, requests
from flask import json

from app.views import events, app

class TestEvents(unittest.TestCase):
    def setUp(self):
        self.req = app.test_client()
        self.events = events

    def tearDown(self):
        self.events.clear()
        self.events = None

    def get_events(self):
      return self.req.get('/api/events')

    def add_event(self, data={}):
      return self.req.post('/api/events', 
        data=json.dumps(data), 
        content_type='application/json'
        )

    def test_initial_events(self):
        r = self.get_events()
        self.assertEqual(r.status_code, 200, 'Status Code not 200')
        body = json.loads(r.data)
        print(("imported events", self.events))
        print(("response events", body.get('events', [])))
        self.assertEqual(self.events, body.get('events', []), 'Events array not equal')

    def test_add_event(self):
        event = {
            "title": "YO",
            "location": 'NRB'
        }
        r = self.add_event(event)
        self.assertEqual(r.status_code, 201, 'Status Code not 201')
        body = json.loads(r.data)
        self.assertTrue(set(event.items()).issubset(set(body['event'].items())))




if __name__ == "__main__":
    unittest.main()