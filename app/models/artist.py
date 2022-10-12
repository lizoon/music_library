from app import *

from sqlalchemy import Column, ForeignKey, Integer, String, text, UniqueConstraint
from sqlalchemy.orm import relationship


def get_all_artists():
    return [Artist.json(artist_) for artist_ in Artist.query.all()]


class Artist(db.Model):
    __tablename__ = 'artists'
    __table_args__ = (UniqueConstraint('firstname', 'surname'),)

    id = Column(Integer, primary_key=True, server_default=text("nextval('artists_id_seq'::regclass)"))
    firstname = Column(String(25), nullable=False)
    surname = Column(String(25))
    genre_id = Column(ForeignKey('genres.id', ondelete='SET NULL'), nullable=False)

    genre = relationship('Genre')

    def __repr__(self):
        if self.surname is not None:
            return f'{self.firstname} {self.surname}'
        return f'{self.firstname}'

    def json(self):
        if self.surname is not None:
            return {'id': self.id,
                    'firstname': self.firstname,
                    'surname': self.surname,
                    'genre_id': self.genre_id}
        return {'id': self.id,
                'firstname': self.firstname,
                'genre_id': self.genre_id}

    def get_artist(id_):
        return [Artist.json(db.session.query(Artist).filter(Artist.id == id_).first())]

    def add_artist(firstname, surname, genre_id):
        new_artist = Artist()
        new_artist.firstname = firstname
        if surname is not "":
            new_artist.surname = surname
        new_artist.genre_id = genre_id
        db.session.add(new_artist)
        db.session.commit()

    def update_artist(id_, firstname, surname, genre_id):
        artist_to_update = db.session.query(Artist).filter(Artist.id == id_).first()
        artist_to_update.firstname = firstname
        if surname is not "":
            artist_to_update.surname = surname
        artist_to_update.artist_id = genre_id
        db.session.commit()

    def delete_artist(id_):
        db.session.query(Artist).filter(Artist.id == id_).delete()
        db.session.commit()
