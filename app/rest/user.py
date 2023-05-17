from app.models.user import *
from app.rest.__init__ import *


@app.route('/users', methods=['GET'])
def get_users():
    try:
        return jsonify({'Users': get_all_users()})
    except Exception:
        return jsonify({"status": "Error", "description": "No users"})


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        return_value = Song.get_user(id)
        return jsonify(return_value)
    except Exception:
        return jsonify({"status": "Error", "description": "No user"})


@app.route('/users', methods=['POST'])
def add_user():
    try:
        request_data = request.get_json()
        Song.add_user(request_data['nickname'],
                      request_data['email'],
                      request_data['password'],
                      request_data['active'])
        response = Response("Ok. User added", 201, mimetype='application/json')
        return response
    except Exception:
        return Response("Error", 404, mimetype='application/json')


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        request_data = request.get_json()
        Song.update_user(id, request_data['nickname'],
                         request_data['email'],
                         request_data['password'],
                         request_data['active'])
        response = Response("Ok. User updated", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        Song.delete_user(id)
        response = Response("Ok. User deleted", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response


