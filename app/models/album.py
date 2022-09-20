from app import *


class Album(db.Model):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, server_default=text("nextval('albums_id_seq')"))
    name = Column(String(20), server_default=text("'New Album'::text"))
    release_year = Column(Integer)
    artist_id = Column(ForeignKey('artists.id', ondelete='CASCADE'), nullable=False)
    cover = Column(String, server_default=text("'/home/liza/PycharmProjects/laba_1/app/static/img/default_.png'::text"))

    artist = relationship('Artist') # add attrs to models для доступа к данным, (name of responsible class for ONE relation)

    def __init__(self, name, release_year, artist_id):
        self.name = name
        self.release_year = release_year
        self.artist_id = artist_id

    def __repr__(self):
        return f'{self.name}'
