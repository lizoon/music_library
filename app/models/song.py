from sqlalchemy.orm import relationship
from sqlalchemy import Sequence

from app import *
from app.models.users_songs import t_users_songs


class Song(db.Model):

    __tablename__ = 'songs'

    id = Column(Integer, Sequence("albums_id_seq"), primary_key=True)
    name = Column(String(80), nullable=False)
    duration = Column(Time, nullable=False)
    album_id = Column(ForeignKey('albums.id', ondelete='CASCADE'), nullable=False)

    album = relationship('Album')
    users = relationship('User', secondary=t_users_songs)

    def __repr__(self):
        return f'{self.name}'
