import pytest
from app.models.artist import Artist
from app.models.genre import Genre
from app import db


def test_artist_attrs(init_test_data, session):
    artist = db.session.query(Artist).first()

    assert hasattr(artist, 'firstname')
    assert isinstance(artist.firstname, str)
    assert 25 >= len(artist.firstname) >= 0

    assert hasattr(artist, 'surname')
    assert isinstance(artist.surname, str)

    assert hasattr(artist, 'genre_id')
    assert isinstance(artist.genre_id, int)
    assert artist.genre_id is not None

# @pytest.mark.parametrize('firstname, surname, genre_id', [
#     ('John', 'Doe', 1),
#     ('Jane', 'Smith', 1),
#     ('Mike', 'Johnson', 1),
# ])
# def test_create_artist(init_test_data, session, firstname, surname, genre_id):
#     artist = Artist(firstname=firstname, surname=surname, genre_id=genre_id)
#     session.add(artist)
#     session.commit()
#     assert artist.id is not None
#     assert artist.firstname == firstname
#     assert artist.surname == surname
#     assert artist.genre_id == genre_id
#     artist = session.query(Artist).first()
#     genre = Genre.query.get(genre_id)
#     assert genre is not None
#     assert artist.genre == genre

# def test_create_artist_without_surname(valid_artist, init_objects):
#     artist = db.session.query(Artist).filter(Artist.firstname == valid_artist.firstname and Artist.surname == valid_artist.surname).first()
#     new_artist = Artist(firstname='NewFirstname', genre_id=artist.genre_id)
#     db.session.add(new_artist)
#     db.session.commit()
#     assert new_artist.id is not None
#     assert new_artist.firstname is not None
#     assert new_artist.surname is None
#     assert new_artist.genre_id is not None
#     db.session.delete(new_artist)
#     db.session.commit()
#
#

def test_get_artist(init_test_data, session):
    # assume
    if not session.query(Genre).first():
        pytest.skip('genre is none')
    artist = db.session.query(Artist).first()
    assert artist.id is not None
    assert artist.firstname is not None
    assert artist.surname is not None
    assert artist.genre_id is not None

#
# def test_update_artist(valid_artist, init_objects):
#     artist = db.session.query(Artist).filter(Artist.firstname == valid_artist.firstname and Artist.surname == valid_artist.surname).first()
#     assert artist.id is not None
#
#     artist.firstname = 'NewName'
#     artist.surname = 'NewSurname'
#     assert artist.firstname == 'NewName'
#     assert artist.surname == 'NewSurname'
#
#
# def test_delete_song(init_objects, valid_artist):
#     artist = db.session.query(Artist).filter(Artist.firstname == valid_artist.firstname and Artist.surname == valid_artist.surname).first()
#     new_artist = Artist(firstname='NewName', surname='NewSurname', genre_id=artist.genre_id)
#     db.session.add(new_artist)
#     db.session.commit()
#     assert new_artist.id is not None
#
#     db.session.delete(new_artist)
#     db.session.commit()
#
#     deleted_artist = db.session.query(Artist).get(new_artist.id)
#     assert deleted_artist is None
#
# def test_invalid_artist(invalid_artist):
#     with pytest.raises(Exception):
#         try:
#             db.session.add(invalid_artist)
#             db.session.commit()
#         except Exception:
#             db.session.rollback()
#             raise
#
# def test_valid_song(valid_artist, init_objects):
#     artist = db.session.query(Artist).filter(Artist.firstname == valid_artist.firstname and Artist.surname == valid_artist.surname).first()
#     genre = db.session.query(Genre).filter(Genre.id == artist.genre_id).first()
#     new_artist = Artist(firstname='NewFirstname', surname='NewSurname', genre_id=genre.id)
#     db.session.add(new_artist)
#     db.session.commit()
#     assert new_artist.id is not None
#     db.session.delete(new_artist)
#     db.session.commit()
#
#
#
