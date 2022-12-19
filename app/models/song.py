from app import *
from app.models.users_songs import t_users_songs

from sqlalchemy import Column, ForeignKey, Integer, Time, String, text
from sqlalchemy.orm import relationship


def get_all_songs():
    return [Song.json(song_) for song_ in Song.query.all()]


class Song(db.Model):

    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, server_default=text("nextval('songs_id_seq'::regclass)"))
    name = Column(String(80), nullable=False)
    album_id = Column(ForeignKey('albums.id', ondelete='CASCADE'), nullable=False)
    path = Column(String)
    type = Column(String)

    album = relationship('Album')
    users = relationship('User', secondary=t_users_songs)

    def __repr__(self):
        return f'{self.name}'

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'duration': self.duration.isoformat(),
                'album_id': self.album_id}

    def get_song(id_):
        return [Song.json(db.session.query(Song).filter(Song.id == id_).first())]

    def add_song(name, duration, album_id):
        new_song = Song()
        new_song.name = name
        new_song.duration = duration
        new_song.album_id = album_id
        db.session.add(new_song)
        db.session.commit()

    def update_song(id_, name, duration, album_id):
        song_to_update = db.session.query(Song).filter(Song.id == id_).first()
        song_to_update.name = name
        song_to_update.duration = duration
        song_to_update.album_id = album_id
        db.session.commit()

    def delete_song(id_):
        db.session.query(Song).filter(Song.id == id_).delete()
        db.session.commit()
