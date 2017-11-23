#!/bin/env python
# -*- coding: utf-8 -*-
"""import depancies."""
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

from data import events

app = Flask(__name__)

auth = HTTPBasicAuth()

events = events = [
    {
        'id': 1,
        'title': u'Mango Harvest',
        'location':u'Kitui, Kenya',
        'time':u'11:00AM',
        'date':u'25 NOV 2017',
        'description': u'Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s,', 
        'done': False,
        'rsvp': [
            {
            'user_id': 1,
            'name': u'John Doe',
            'email': u'john.D@gmail.com'
            },
            {
            'user_id': 3,
            'name': u'Antony Ng\'ang\'a',
            'email': u'tonny.nesh@gmail.com'
            }
        ]
    },
    {
        'id': 2,
        'title': u'Python Meetup',
        'location':u'Nairobi, Kenya',
        'time':u'07:00PM',
        'date':u'30 NOV 2017',
        'description': u'Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s,', 
        'done': False,
        'rsvp': [
            {
            'user_id': 2,
            'name': u'Mary Jane',
            'email': u'jane.mary@yahoo.com'
            }
        ]
    }
]


@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify({'events': events})

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Fetch single Event."""
    for event in events:
      	if event['id'] == event_id:
    	    return jsonify({'event': event})
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create new event."""
    if not request.json or not 'title' in request.json:
        abort(400)
    event = {
        'id': events[-1]['id'] + 1,
        'title': request.json['title'],
        'location':request.json.get('location', ""),
        'time':request.json.get('time', ""),
        'date':request.json.get('date', ""),
        'description': request.json.get('description', ""),
        'done': False
    }
    events.append(event)
    return jsonify({'event': event}), 201

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event."""
    for event in events:
        if event['id'] == event_id and request.json:
            event[0]['title'] = request.json.get('title', event[0]['title'])
            event[0]['location'] = request.json.get('location', event[0]['location'])
            event[0]['time'] = request.json.get('time', event[0]['time'])
            event[0]['date'] = request.json.get('date', event[0]['date'])
            event[0]['description'] = request.json.get('description', event[0]['description'])
            event[0]['done'] = request.json.get('done', event[0]['done'])
            return jsonify({'event': event[0]})
      
        abort(404)

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Build the cookiecutter."""
    for event in events:
        if event['id'] == event_id:
            events.remove(event[0])
        return jsonify({'result': True})
    abort(404)

@auth.get_password
def get_password(username):
    if username == 'john':
        return 'doe'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    app.run(debug=True)