#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

events = [
    {
        'id': 1,
        'title': u'Mango Harvest',
        'location':u'Kitui, Kenya',
        'time':u'11:00AM',
        'date':u'25 NOV 2017',
        'description': u'Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s,', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Python Meetup',
        'location':u'Nairobi, Kenya',
        'time':u'07:00PM',
        'date':u'30 NOV 2017',
        'description': u'Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s,', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/events', methods=['GET'])
def get_events():
    return jsonify({'events': events})

@app.route('/todo/api/v1.0/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = [event for event in events if event['id'] == event_id]
    if len(event) == 0:
        abort(404)
    return jsonify({'event': event[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/events', methods=['POST'])
def create_event():
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

if __name__ == '__main__':
    app.run(debug=True)