import datetime

import pytest
from app import create_app, db, User, Genre, Album, Artist, Song
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

def pytest_sessionstart(session):
    # Since flask_sqlalchemy.SQLAlchemy uses hardcoded config keys, we have no choice but to override
    # SQLALCHEMY_DATABASE_URI with a test DB URI
    from app.config import Configuration
    Configuration.SQLALCHEMY_DATABASE_URI = Configuration.SQLALCHEMY_TEST_DATABASE_URI


@pytest.fixture(autouse=True)
def flask_client():
    """An application for the tests"""
    from app import app
    app.config["TESTING"] = True
    yield app


@pytest.yield_fixture(scope="function", autouse=True)
def init_db():
    from app import app, db

    Session = sessionmaker(bind=db.engine)
    session = Session()

    db.create_all("__all__", app)

    try:
        session.begin()
        yield session
        session.rollback()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    db.drop_all()

@pytest.fixture()
def init_session():
    Session = sessionmaker()
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def init_objects(flask_client, valid_user, valid_genre, valid_album, valid_artist, valid_song):
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

