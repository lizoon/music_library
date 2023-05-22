import datetime

import pytest
from app.models.song import Song
from app.models.album import Album
from app.models.user import User
from app.models.users_songs import t_users_songs


def test_song_attrs(init_test_data, session):
    song = session.query(Song).first()
    assert hasattr(song, 'name')
    assert isinstance(song.name, str)
    assert len(song.name) >= 0

    assert hasattr(song, 'duration')
    assert isinstance(song.duration, datetime.time)
    assert song.duration is not None

    assert hasattr(song, 'album_id')
    assert isinstance(song.album_id, int)
    assert song.album_id is not None

def test_create_song(init_test_data, session):
    # assume
    if not session.query(Album).first():
        pytest.skip('album is none')

    song = session.query(Song).first()
    assert song.id is not None
    assert song.album_id is not None
    new_song = Song(name='NewSong', duration=datetime.time(0, 3, 41), album_id=song.album_id)
    session.add(new_song)
    session.commit()
    assert new_song.id is not None
    assert new_song.name == 'NewSong'
    assert new_song.duration == datetime.time(0, 3, 41)
    assert new_song.album_id == song.album_id


def test_get_song(init_test_data, session):
    # assume
    if not session.query(Album).first():
        pytest.skip('album is none')

    test_create_song(init_test_data, session)
    song = session.query(Song).first()
    assert song.id is not None
    assert song.name == 'TestName'
    assert song.duration == datetime.time(0, 3, 48)
    assert song.album_id is not None


def test_update_song(init_test_data, session):
    # assume
    if not session.query(Album).first():
        pytest.skip('album is none')

    song = session.query(Song).first()
    assert song.id is not None

    song.name = 'NewName'
    song.duration = datetime.time(0, 2, 39)
    session.commit()
    upd_song = session.query(Song).filter(Song.id == song.id).first()
    assert upd_song.name == 'NewName'
    assert upd_song.duration == datetime.time(0, 2, 39)
    assert upd_song.album_id is not None


def test_delete_song(init_test_data, session):
    # assume
    if not session.query(Album).first():
        pytest.skip('album is none')

    song = session.query(Song).first()
    assert song is not None

    session.delete(song)
    session.commit()

    deleted_song = session.query(Song).filter_by(id=song.id).first()
    assert deleted_song is None

def test_invalid_song(invalid_song, session):
    with pytest.raises(Exception):
        try:
            session.add(invalid_song)
            session.commit()
        except Exception:
            session.rollback()
            raise

def test_valid_song(init_test_data, session):
    album = session.query(Album).first()
    new_song = Song(name='NewSong', duration=datetime.time(0,3,20), album_id=album.id)
    session.add(new_song)
    session.commit()
    assert new_song.id is not None
    assert new_song.name == 'NewSong'
    assert new_song.duration == datetime.time(0,3,20)


def test_song_album_relation(init_test_data, session):
    song = session.query(Song).first()
    assert song.id is not None
    album = session.query(Album).first()
    assert album.id is not None
    assert song.album == album
    assert song.album_id == album.id

def test_song_user_relation(init_test_data, session):
    song = session.query(Song).first()
    assert song.id is not None

    user = User(password='testtest', email='test2@gmail.com', nickname='test2')
    session.add(user)
    session.commit()
    assert user.id is not None

    session.execute(t_users_songs.insert().values(user_id=user.id, song_id=song.id))
    session.commit()
    assert song.users == [user]


