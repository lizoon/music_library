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

@pytest.mark.parametrize('firstname, surname, genre_id', [
    ('Test1', 'Test1', 1),
    ('Test2', 'Test2', 1),
    ('Test3', 'Test3', 1),
])
def test_create_artist(firstname, surname, genre_id, init_test_data, session):
    artist = Artist(firstname=firstname, surname=surname, genre_id=genre_id)
    session.add(artist)
    session.commit()
    assert artist.id is not None
    assert artist.firstname == firstname
    assert artist.surname == surname
    assert artist.genre_id == genre_id
    artist = session.query(Artist).first()
    genre = Genre.query.get(genre_id)
    assert artist.genre is not None
    assert artist.genre_id == genre.id


@pytest.mark.parametrize('firstname, genre_id', [
    ('Test1', 1),
    ('Test2', 1),
    ('Test3', 1),
])
def test_create_artist_without_surname(firstname, genre_id, init_test_data, session):
    artist = Artist(firstname=firstname, genre_id=genre_id)
    session.add(artist)
    session.commit()
    assert artist.id is not None
    assert artist.firstname == firstname
    assert artist.surname is None
    assert artist.genre_id == genre_id
    artist = session.query(Artist).first()
    genre = Genre.query.get(genre_id)
    assert artist.genre is not None
    assert artist.genre_id == genre.id



def test_get_artist(init_test_data, session):
    # assume
    if not session.query(Genre).first():
        pytest.skip('genre is none')
    artist = db.session.query(Artist).first()
    assert artist.id is not None
    assert artist.firstname is not None
    assert artist.surname is not None
    assert artist.genre_id is not None


@pytest.mark.parametrize('old_artist, new_artist', [
    ({'firstname': 'Test1', 'surname': 'Test1', 'genre_id': 1},
    {'firstname': 'NewTest1', 'surname': 'NewTest1', 'genre_id': 1}),
    ({'firstname': 'Test2', 'surname': 'Test2', 'genre_id': 1},
     {'firstname': 'NewTest2', 'surname': 'NewTest2', 'genre_id': 1}),
    ({'firstname': 'Test3', 'surname': 'Test3', 'genre_id': 1},
     {'firstname': 'NewTest3', 'surname': 'NewTest3', 'genre_id': 1}),
])
def test_update_artist(old_artist, new_artist, init_test_data, session):
    artist = Artist(firstname=old_artist['firstname'], surname=old_artist['surname'], genre_id=old_artist['genre_id'])
    session.add(artist)
    session.commit()

    assert artist.id is not None

    artist.firstname = new_artist['firstname']
    artist.surname = new_artist['surname']
    session.commit()

    assert artist.id is not None
    assert artist.firstname == new_artist['firstname']
    assert artist.surname == new_artist['surname']
    assert artist.genre_id is not None


def test_delete_song(init_test_data, session):
    artist = session.query(Artist).first()
    assert artist.id is not None
    session.delete(artist)
    session.commit()
    deleted_artist = session.query(Artist).first()
    assert deleted_artist is None

def test_invalid_artist(invalid_artist):
    with pytest.raises(Exception):
        try:
            db.session.add(invalid_artist)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


def test_artist_genre_relation(init_test_data, session):
    artist = session.query(Artist).first()
    assert artist.id is not None
    genre = session.query(Genre).first()
    assert genre.id is not None
    assert artist.genre == genre

