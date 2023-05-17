from sqlalchemy.orm import relationship

from app import *

from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship


def get_all_albums():
    return [Album.json(album_) for album_ in Album.query.all()]


class Album(db.Model):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, server_default=text("nextval('albums_id_seq')"))
    name = Column(String(20), server_default=text("'New Album'::text"))
    release_year = Column(Integer)
    artist_id = Column(ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    cover = Column(String)

    artist = relationship('Artist') # add attrs to models для доступа к данным, (name of responsible class for ONE relation)

    def __repr__(self):
        return f'{self.name}'

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'release_year': self.release_year,
                'artist_id': self.artist_id}

    def get_album(id_):
        return [Album.json(db.session.query(Album).filter(Album.id == id_).first())]

    def add_album(name, release_year, artist_id):
        new_genre = Album()
        new_genre.name = name
        new_genre.release_year = release_year
        new_genre.artist_id = artist_id
        db.session.add(new_genre)
        db.session.commit()

    def update_album(id_, name, release_year, artist_id):
        album_to_update = db.session.query(Album).filter(Album.id == id_).first()
        album_to_update.name = name
        album_to_update.release_year = release_year
        album_to_update.artist_id = artist_id
        db.session.commit()

    def delete_album(id_):
        db.session.query(Album).filter(Album.id == id_).delete()
        db.session.commit()
