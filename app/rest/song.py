import datetime

from app.models.song import *
from app.rest.__init__ import *


@app.route('/songs', methods=['GET'])
def get_songs():
    try:
        return jsonify({'Songs': get_all_songs()})
    except Exception:
        return jsonify({"status": "Error", "description": "No songs"})


@app.route('/songs/<id>', methods=['GET'])
def get_song(id):
    try:
        return_value = Song.get_song(id)
        return jsonify(return_value)
    except Exception:
        return jsonify({"status": "Error", "description": "No song"})


@app.route('/songs', methods=['POST'])
def add_song():
    try:
        request_data = request.get_json()
        Song.add_song(request_data['name'],
                  datetime.time.fromisoformat(request_data['duration']),
                  request_data['album_id'])
        response = Response("Ok. Song added", 201, mimetype='application/json')
        return response
    except Exception:
        return Response("Error", 404, mimetype='application/json')


@app.route('/songs/<id>', methods=['PUT'])
def update_song(id):
    try:
        request_data = request.get_json()
        Song.update_song(id, request_data['name'],
                        datetime.time.fromisoformat(request_data['duration']),
                        request_data['album_id'])
        response = Response("Ok. Song updated", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response


@app.route('/songs/<id>', methods=['DELETE'])
def delete_song(id):
    try:
        Song.delete_song(id)
        response = Response("Ok. Song deleted", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response

