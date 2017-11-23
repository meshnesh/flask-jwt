import unittest

import os

import run

class TestEvents(unittest.TestCase):

    def test_create_event(self):
        resp = self.client().post('/api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('andela bootcamp', str(resp.data))
    
    def test_update_event(self):
        resp = self.client().post('api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().put('/api/events/1/', 
                data={"text":"andela bootcamp cohort 24"})
        self.assertEqual(resp.status_code, 200)
        new_ = self.client().get('api/events/1/')
        self.assertIn('cohort', str(new_.data))


if __name__ == '__main__':
    unittest.main()