import pytest
from hamcrest import (
    all_of, any_of, has_entry, has_properties, has_length,
    contains, has_item, contains_inanyorder, not_, matches_regexp, assert_that, equal_to, contains_string, not_none)
from app.models.user import User, Role, t_roles_users
from app.models.song import Song
from app.models.users_songs import t_users_songs

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


@pytest.mark.parametrize('nickname, email, password', [
    ('Test1', 'Test1@gmail.com', 'Test1'),
    ('Test2', 'Test2@gmail.com', 'Test2'),
    ('Test3', 'Test3@gmail.com', 'Test3'),
])
def test_create_user(nickname, email, password, session):
    user = User(nickname=nickname, email=email, password=password)
    session.add(user)
    session.commit()
    assert user.password == nickname
    assert user.email == email
    assert user.nickname == password
    assert not user.is_anonymous
    assert user.id is not None


@pytest.mark.parametrize('nickname, email, password', [
    ('Test1', 'Test1@gmail.com', 'Test1'),
    ('Test2', 'Test2@gmail.com', 'Test2'),
    ('Test3', 'Test3@gmail.com', 'Test3'),
])
def test_get_user(nickname, email, password, session):
    test_create_user(nickname, email, password, session)
    user = session.query(User).filter(User.email == email).first()
    assert user.id is not None
    assert user.password is not None
    assert user.nickname is not None
    assert user.email is not None


@pytest.mark.parametrize('nickname, email, password', [
    ('Test1', 'Test1@gmail.com', 'Test1'),
    ('Test2', 'Test2@gmail.com', 'Test2'),
    ('Test3', 'Test3@gmail.com', 'Test3'),
])
def test_update_user(nickname, email, password, session):
    test_create_user(nickname, email, password, session)
    user = session.query(User).filter(User.email == email).first()
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

@pytest.mark.parametrize('nickname, email, password', [
    ('Test1', 'Test1@gmail.com', 'Test1'),
    ('Test2', 'Test2@gmail.com', 'Test2'),
    ('Test3', 'Test3@gmail.com', 'Test3'),
])
def test_delete_user(nickname, email, password, session):
    test_create_user(nickname, email, password, session)
    user = session.query(User).filter(User.email == email).first()
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


@pytest.mark.parametrize('admin', [
    {'nickname': 'Admin1', 'email': 'Admin1@gmail.com', 'password': 'Admin1'},
    {'nickname': 'Admin2', 'email': 'Admin2@gmail.com', 'password': 'Admin2'},
    {'nickname': 'Admin3', 'email': 'Admin3@gmail.com', 'password': 'Admin3'}
])
def test_many_admin_user(admin, session):
    user = User(password=admin['password'], email=admin['email'], nickname=admin['nickname'], active=True)
    role = Role(name='admin')
    session.add(user)
    session.add(role)
    session.commit()
    session.execute(t_roles_users.insert().values(user_id=user.id, role_id=role.id))

    assert_that(user, all_of(
        has_properties(
            email=contains_string('@gmail.com'),
            active=not_none(),
            password=not_none(),
            nickname=contains_string('Admin')
        ),
    ))


def test_users_songs_relation(init_test_data, user_datastore, session):
    user = User(password='testtest', email='test2@gmail.com', nickname='test2')
    session.add(user)
    session.commit()
    song = session.query(Song).first()
    session.execute(t_users_songs.insert().values(user_id=user.id, song_id=song.id))
    session.commit()

    s = session.query(Song).get(song.id)
    assert s.users == [user]





