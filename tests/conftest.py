import datetime

import pytest
from app import create_app, db, User, Genre, Album, Artist, Song
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def test_client():
    """An application for the tests"""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture()
def init_session(test_client):
    Session = sessionmaker()
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def init_objects(test_client, valid_user, valid_genre, valid_album, valid_artist, valid_song):
    Session = sessionmaker()
    session = Session()
    db.session.add(valid_user)
    db.session.add(valid_genre)
    db.session.add(valid_album)
    db.session.add(valid_artist)
    db.session.add(valid_song)
    db.session.commit()
    yield session
    db.session.add(valid_user)
    db.session.add(valid_genre)
    db.session.add(valid_album)
    db.session.add(valid_artist)
    db.session.add(valid_song)
    db.session.commit()
    session.close()


@pytest.fixture()
def valid_user():
    yield User(password='testtest',
               email='test2@gmail.com',
               nickname='test2')

@pytest.fixture()
def invalid_user():
    yield User(password='',
               email='test.gmail.com',
               nickname='bigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbig')


@pytest.fixture()
def valid_genre():
    yield Genre(name='TestGenre')



@pytest.fixture()
def valid_album():
    yield Album(name='TestAlbum',
                release_year='1999',
                artist_id=None)



@pytest.fixture()
def valid_artist():
    yield Artist(firstname='TestFirstName',
                 surname='TestSurname',
                 genre_id=None)



@pytest.fixture()
def valid_song():
    yield Song(name='TestName',
               duration=datetime.time(0,3,48),
               album_id=None)


@pytest.fixture()
def invalid_song():
    yield Song(name='FailedTestName',
               duration=datetime.time(0,0,0),
               album_id=None)

