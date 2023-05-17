import pytest
from app.models.user import User
import re
from app import db

def test_user_attrs(valid_user):
    assert hasattr(valid_user, 'password')
    assert isinstance(valid_user.password, str)
    assert len(valid_user.password) >= 0

    assert hasattr(valid_user, 'email')
    assert isinstance(valid_user.email, str)
    assert 60 >= len(valid_user.email) >= 0
    query_result = User.query.filter_by(email=valid_user.email).count()
    assert query_result == 0
    assert re.match(r'^[a-zA-Z0-9]+[._]?[a-z 0-9]+@\w+[.]\w{2,3}$', valid_user.email) is not None

    assert hasattr(valid_user, 'nickname')
    assert isinstance(valid_user.nickname, str)
    assert 20 >= len(valid_user.nickname) >= 0

    assert hasattr(valid_user, 'active')
    assert isinstance(valid_user.active, bool)


def test_create_user():
    user = User(password='testtest',
                email='test2@gmail.com',
                nickname='test2')
    assert user.password == 'testtest'
    assert user.email == 'test2@gmail.com'
    assert user.nickname == 'test2'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous
    db.session.add(user)
    db.session.commit()
    assert user.id is not None
    db.session.delete(user)
    db.session.commit()


def test_get_user():
    user_id = 2
    user = User.query.filter_by(id=user_id).first()
    assert user.password == 'admin'
    assert user.nickname == 'admin'
    assert user.email == 'admin@gmail.com'
    assert user.active == True

def test_update_user(valid_user):
    db.session.add(valid_user)
    db.session.commit()
    assert valid_user.id is not None
    user = db.session.query(User).filter(User.id == valid_user.id).first()
    user.password = 'new_password'
    user.email = 'new_email@gmail.com'
    user.nickname = 'new_nickname'
    assert user.password == 'new_password'
    assert user.email == 'new_email@gmail.com'
    assert user.nickname == 'new_nickname'
    db.session.delete(valid_user)
    db.session.commit()

def test_delete_user(valid_user):
    db.session.add(valid_user)
    db.session.commit()
    assert valid_user.id is not None
    db.session.delete(valid_user)
    db.session.commit()
    q = db.session.query(User).filter(User.id == valid_user.id).first()
    assert q is None



def test_invalid(invalid_user):
    with pytest.raises(Exception):
        try:
            db.session.add(invalid_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

def test_valid_attrs_user(valid_user):
    db.session.add(valid_user)
    db.session.commit()
    assert valid_user.id is not None
    db.session.delete(valid_user)
    db.session.commit()



