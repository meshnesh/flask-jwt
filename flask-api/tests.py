import requests, unittest

from data import events
from app import app
class TestEvents(unittest.TestCase):
  def setUp(self):
    app.run(debug=True)

  def tearDown(self):
    pass

  def test_get_events(self):
    events_res =  request.get(
      'http://localhost:{port}/todo/api/v1.0/events'.format(
      port=4000
    ))
    self.assertCountEqual(events_res.json(), events, msg="Events be real")