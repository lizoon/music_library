from app.models.album import *
from app.rest.__init__ import *


@app.route('/albums', methods=['GET'])
def get_albums():
    try:
        return jsonify({'Genres': get_all_albums()})
    except Exception:
        return jsonify({"status": "Error", "description": "No albums"})


@app.route('/albums/<id>', methods=['GET'])
def get_album(id):
    try:
        return_value = Album.get_album(id)
        return jsonify(return_value)
    except Exception:
        return jsonify({"status": "Error", "description": "No album"})


@app.route('/albums', methods=['POST'])
def add_album():
    try:
        request_data = request.get_json()
        Album.add_album(request_data['name'], request_data['release_year'], request_data['artist_id'])
        response = Response("Ok. Album added", 201, mimetype='application/json')
        return response
    except Exception:
        return Response("Error", 404, mimetype='application/json')


@app.route('/albums/<id>', methods=['PUT'])
def update_album(id):
    try:
        request_data = request.get_json()
        Album.update_album(id, request_data['name'], request_data['release_year'], request_data['artist_id'])
        response = Response("Ok. Album updated", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response


@app.route('/albums/<id>', methods=['DELETE'])
def delete_album(id):
    try:
        Album.delete_album(id)
        response = Response("Ok. Album deleted", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response

