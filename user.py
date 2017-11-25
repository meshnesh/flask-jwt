#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

users = [
    {
        'user_id': 1,
        'name': u'John Doe',
        'email': u'john.D@gmail.com'
    },
    {
        'user_id': 2,
        'name': u'Mary Jane',
        'email': u'jane.mary@yahoo.com'
    },
    {
        'user_id': 3,
        'name': u'Antony Ng\'ang\'a',
        'email': u'tonny.nesh@gmail.com'
    }
]

@app.route('/api/users/v1/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/api/auth/login/<int:user_id>', methods=['POST'])
def user_login(user_id):
    for user in users:
      	if user['id'] == user_id:
    	    return jsonify({'users': users[0]})
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/auth/register', methods=['POST'])
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

@app.route('/api/auth/login/<int:user_id>', methods=['POST'])
def user_logout(user_id):
    for user in users:
      	if user['id'] == user_id:
    	    return jsonify({'users': users})
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)