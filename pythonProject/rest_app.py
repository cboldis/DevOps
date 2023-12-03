from flask import Flask, request

import db_connector

app = Flask(__name__)


@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    if request.method == 'GET':
        name = db_connector.get_user_name(user_id)
        if name != -1:
            return {'user_id': user_id, 'user_name': name}, 200
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500
    elif request.method == 'POST':
        request_data = request.json
        user_name = request_data.get('user_name')
        if db_connector.insert(user_name, user_id) == 0:
            return {'status': 'ok', 'user_added': user_name}, 200
        else:
            return {'status': 'error', 'reason': 'id already exists'}, 500
    elif request.method == 'PUT':
        request_data = request.json
        user_name = request_data.get('user_name')
        if db_connector.update(user_name, user_id) == 0:
            return {'status': 'ok', 'user_updated': user_name}, 200
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500
    elif request.method == 'DELETE':
        if db_connector.delete(user_id) == 0:
            return {'status': 'ok', 'user_deleted': user_id}, 200
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500


app.run(host='127.0.0.1', debug=True, port=5000)
