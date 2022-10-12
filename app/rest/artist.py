from app.models.artist import *
from app.rest.__init__ import *


@app.route('/artists', methods=['GET'])
def get_artists():
    try:
        return jsonify({'Artists': get_all_artists()})
    except Exception:
        return jsonify({"status": "Error", "description": "No artists"})


@app.route('/artists/<id>', methods=['GET'])
def get_artist(id):
    try:
        return_value = Artist.get_artist(id)
        return jsonify(return_value)
    except Exception:
        return jsonify({"status": "Error", "description": "No artist"})


@app.route('/artists', methods=['POST'])
def add_artist():
    try:
        request_data = request.get_json()
        if 'surname' in request_data:
            Artist.add_artist(request_data['firstname'], request_data['surname'], request_data['genre_id'])
        else:
            Artist.add_artist(request_data['firstname'], "", request_data['genre_id'])

        response = Response("Ok. Artist added", 201, mimetype='application/json')
        return response
    except Exception:
        return Response("Error", 404, mimetype='application/json')


@app.route('/artists/<id>', methods=['PUT'])
def update_artist(id):
    try:
        request_data = request.get_json()
        if 'surname' in request_data:
            Artist.update_artist(id, request_data['firstname'], request_data['surname'], request_data['genre_id'])
        else:
            Artist.update_artist(id, request_data['firstname'], "", request_data['genre_id'])

        response = Response("Ok. Artist updated", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response


@app.route('/artists/<id>', methods=['DELETE'])
def delete_artist(id):
    try:
        Artist.delete_artist(id)
        response = Response("Ok. Artist deleted", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response

