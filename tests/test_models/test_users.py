import pytest
from hamcrest import assert_that, matches_regexp
from app.models.user import User, Role
import re

def test_user_attrs(valid_user):
    assert hasattr(valid_user, 'password')
    assert isinstance(valid_user.password, str)
    assert len(valid_user.password) >= 0

    assert hasattr(valid_user, 'email')
    assert isinstance(valid_user.email, str)
    assert 60 >= len(valid_user.email) >= 0
    query_result = User.query.filter_by(email=valid_user.email).count()
    assert query_result is not None

    assert_that(valid_user.email, matches_regexp(r'^[a-zA-Z0-9]+[._]?[a-z 0-9]+@\w+[.]\w{2,3}$'))

    assert hasattr(valid_user, 'nickname')
    assert isinstance(valid_user.nickname, str)
    assert 20 >= len(valid_user.nickname) >= 0

    assert hasattr(valid_user, 'active')
    assert isinstance(valid_user.active, bool)


def test_create_user(session):
    valid_user = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)
    session.add(valid_user)
    session.commit()
    assert valid_user.password == 'testtest'
    assert valid_user.email == 'test2@gmail.com'
    assert valid_user.nickname == 'test2'
    assert valid_user.is_authenticated
    assert valid_user.is_active
    assert not valid_user.is_anonymous
    assert valid_user.id is not None


def test_get_user(session):
    test_create_user(session)
    user = session.query(User).first()
    assert user.id is not None
    assert user.password is not None
    assert user.nickname is not None
    assert user.email is not None
    assert user.active is not None

def test_update_user(session):
    test_create_user(session)
    user = session.query(User).first()
    assert user.id is not None
    user.password = 'new_password'
    user.email = 'new_email@gmail.com'
    user.nickname = 'new_nickname'
    session.commit()
    upd_user = session.query(User).filter(User.id == user.id).first()
    assert upd_user.id is not None
    assert upd_user.password == 'new_password'
    assert upd_user.email == 'new_email@gmail.com'
    assert upd_user.nickname == 'new_nickname'

def test_delete_user(session):
    test_create_user(session)
    user = session.query(User).first()
    assert user.id is not None
    session.delete(user)
    session.commit()
    q = session.query(User).filter(User.id == user.id).first()
    assert q is None



def test_invalid_user(invalid_user, session):
    with pytest.raises(Exception):
        try:
            session.add(invalid_user)
            session.commit()
        except Exception:
            session.rollback()
            raise

def test_valid_user(valid_user, session):
    session.add(valid_user)
    session.commit()
    assert valid_user.id is not None
    session.delete(valid_user)
    session.commit()


def test_admin_user(user_datastore, session):
    user = user_datastore.create_user(password='admin', email='admin@gmail.com', nickname='admin', active=True)
    role = user_datastore.create_role(name='admin')
    user_datastore.add_role_to_user(user, role)
    user_datastore.commit()
    u = session.query(User).first()
    assert u.id is not None
    assert u.password == 'admin'
    assert u.nickname == 'admin'
    assert u.email == 'admin@gmail.com'
    assert u.is_active
    assert u.has_role('admin')


