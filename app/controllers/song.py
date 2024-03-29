from flask import flash
from werkzeug.exceptions import abort
from app.models.users_songs import *


@app.route('/<prev>/song/<song_id>/add')
def song_add(song_id, prev):
    song = Song.query.get(song_id)

    if song:
        songs = db.session.query(Song).filter(Song.users.any(Song.id == current_user.id))

        if song in songs:
            flash('This song is already added')
            if prev == 'search':
                return redirect(url_for('album', album_id=song.album_id))
            elif prev == 'search_res':
                return redirect(url_for('library'))
            else:
                return redirect(url_for('library'))

        flash('Song {0} liked!'.format(song.name))
        statement = t_users_songs.insert().values(user_id=current_user.id, song_id=song.id)
        db.session.execute(statement)
        db.session.commit()

        if prev == 'search':
            return redirect(url_for('album', album_id=song.album_id))
        else:
            return redirect(url_for('library'))

    abort(404)


@app.route('/<prev>/song/<song_id>/delete')
def song_delete(song_id, prev):
    song = db.session.query(Song).get(song_id)

    if song:
        songs = db.session.query(Song).filter(Song.users.any(Song.id == current_user.id))

        if song not in songs:
            flash('There is no such song!')
            if prev == 'search':
                return redirect(url_for('album', album_id=song.album_id))
            elif prev == 'search_res':
                return redirect(url_for('library'))
            elif prev == 'profile':
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('library'))

        flash('Song {0} deleted!'.format(song.name))
        song.users.remove(current_user)
        db.session.commit()

        if prev == 'search':
            return redirect(url_for('album', album_id=song.album_id))
        elif prev == 'profile':
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('library'))

    abort(404)
