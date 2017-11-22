#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

from data import events

app = Flask(__name__)

auth = HTTPBasicAuth()

events = events


@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify({'events': events})

@app.route('/api/events/<int:event_id>', methods=['GET'])
@auth.login_required
def get_event(event_id):
    for event in events:
      	if event['id'] == event_id:
    	    return jsonify({'event': event[0]})
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/events', methods=['POST'])
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

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
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