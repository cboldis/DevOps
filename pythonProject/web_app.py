from flask import Flask, request

import db_connector

app = Flask(__name__)


@app.route('/users/get_user_data/<user_id>', methods=['GET'])
def get_user_name(user_id):
    if request.method == 'GET':
        name = db_connector.get_user_name(user_id)
        if name != -1:
            return "<H1 id='user'>" + name + "</H1>"
        else:
            return "<H1 id='error'> no such user: " + user_id + "</H1>"


app.run(host='127.0.0.1', debug=True, port=5001)
