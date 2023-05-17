import pytest
from app import create_app, db, User
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
def valid_user():
    yield User(password='testtest',
                email='test2@gmail.com',
                nickname='test2')

@pytest.fixture()
def invalid_user():
    yield User(password='',
               email='test.gmail.com',
               nickname='bigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbigbig')



