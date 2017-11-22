#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

from user_data import users

app = Flask(__name__)

users = users

@app.route('/api/users/v1/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/api/users/v1/users/<int:user_id>', methods=['GET'])
def user_login(user_id):
    for user in users:
      	if user['id'] == user_id:
    	    return jsonify({'users': users[0]})
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/users/v1/users', methods=['POST'])
def user_registration():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name'],
        'email':request.json.get('email', ""),
        'password':request.json.get('password', "")
    }
    users.append(user)
    return jsonify({'users': users}), 201


if __name__ == '__main__':
    app.run(debug=True)