import sys
import datetime
import pytest
from flask_security import SQLAlchemyUserDatastore, Security, RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Boolean
import flask_migrate

from app import create_app, db, User, Genre, Album, Artist, Song, create_db
from sqlalchemy.orm import sessionmaker, relationship
from app.models.user import Role


@pytest.fixture(scope='function')
def application():
    from app import app as _app
    _app.config["TESTING"] = True
    yield _app


@pytest.fixture(scope="function", autouse=True)
def database(application):
    from app import db
    with application.app_context():
        db.engine.execute('DROP TABLE IF EXISTS {} CASCADE;'.format(', '.join(db.metadata.tables.keys())))
        db.engine.execute('DROP TABLE IF EXISTS alembic_version CASCADE;')

        flask_migrate.upgrade()
        yield db


@pytest.fixture(scope='function')
def client(application):
    with application.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def user_datastore(database):
    user_datastore = SQLAlchemyUserDatastore(database, User, Role)
    yield user_datastore


@pytest.fixture(scope="function")
def security(application, user_datastore):
    security = Security(application, user_datastore)
    return security


@pytest.fixture(scope="function")
def session(database):
    Session = sessionmaker(bind=database.engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture()
def init_test_data(user_datastore, session):
    user_datastore.create_user(password='testtest', email='test2@gmail.com', nickname='test2')
    session.commit()

    valid_genre = Genre(name='TestGenre')
    session.add(valid_genre)
    session.commit()

    valid_artist = Artist(firstname='TestFirstName', surname='TestSurname', genre_id=None)
    valid_artist.genre_id = valid_genre.id
    session.add(valid_artist)
    session.commit()

    valid_album = Album(name='TestAlbum', release_year='1999', artist_id=None)
    valid_album.artist_id = valid_artist.id
    session.add(valid_album)
    session.commit()

    valid_song = Song(name='TestName', duration=datetime.time(0,3,48), album_id=None)
    valid_song.album_id = valid_album.id
    session.add(valid_song)
    session.commit()

    yield session

    session.close()


@pytest.fixture()
def valid_user():
    u = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)
    yield u

@pytest.fixture()
def invalid_user():
    u = User(password='', email='test.gmail.com', nickname='bigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbig')
    yield u


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
def invalid_artist():
    yield Artist(firstname='',
                 surname='',
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

