from flask import render_template
from flask_login import login_required
from app.models.users_songs import *


@app.route('/album/<album_id>')
@login_required
def album(album_id):
    album = Album.query.get(album_id)
    songs = Song.query.filter(Song.album_id == album_id).all()
    img = Album.query.filter(album_id==Album.id).with_entities(Album.cover).first()[0]
    return render_template('album.html', title='album', album=album.name, songs=songs, cover=img)

