from app.models.genre import *
from app.rest.__init__ import *


@app.route('/genres', methods=['GET'])
def get_genres():
    try:
        return jsonify({'Genres': get_all_genres()})
    except Exception:
        return jsonify({"status": "Error", "description": "No genres"})


@app.route('/genres/<id>', methods=['GET'])
def get_genre(id):
    try:
        return_value = Genre.get_genre(id)
        return jsonify(return_value)
    except Exception:
        return jsonify({"status": "Error", "description": "No genre"})


@app.route('/genres', methods=['POST'])
def add_genre():
    try:
        request_data = request.get_json()
        Genre.add_genre(request_data['name'])
        response = Response("Ok. Genre added", 201, mimetype='application/json')
        return response
    except Exception:
        return Response("Error", 404, mimetype='application/json')


@app.route('/genres/<id>', methods=['PUT'])
def update_genre(id):
    try:
        request_data = request.get_json()
        Genre.update_genre(id, request_data['name'])
        response = Response("Ok. Genre updated", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response


@app.route('/genres/<id>', methods=['DELETE'])
def delete_genre(id):
    try:
        Genre.delete_genre(id)
        response = Response("Ok. Genre deleted", 200, mimetype='application/json')
        return response
    except Exception:
        response = Response("Error", 404, mimetype='application/json')
        return response

