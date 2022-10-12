from app import *


from sqlalchemy import Column, Integer, String, text


def get_all_genres():
    return [Genre.json(genre_) for genre_ in Genre.query.all()]


class Genre(db.Model):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, server_default=text("nextval('genres_id_seq'::regclass)"))
    name = Column(String(15), nullable=False)

    def __repr__(self):
        return f'{self.name}'

    def json(self):
        return {'id': self.id,
                'name': self.name}

    def get_genre(id_):
        return [Genre.json(db.session.query(Genre).filter(Genre.id == id_).first())]

    def add_genre(name):
        new_genre = Genre()
        new_genre.name = name
        db.session.add(new_genre)
        db.session.commit()

    def update_genre(id_, name):
        genre_to_update = db.session.query(Genre).filter(Genre.id == id_).first()
        genre_to_update.name = name
        db.session.commit()

    def delete_genre(id_):
        db.session.query(Genre).filter(Genre.id == id_).delete()
        db.session.commit()

