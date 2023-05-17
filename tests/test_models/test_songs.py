import datetime

import pytest
from app.models.song import Song
from app.models.album import Album
from app import db

def test_song_attrs(valid_song):
    assert hasattr(valid_song, 'name')
    assert isinstance(valid_song.name, str)
    assert len(valid_song.name) >= 0

    assert hasattr(valid_song, 'duration')
    assert isinstance(valid_song.duration, datetime.time)
    assert valid_song.duration is not None

    assert hasattr(valid_song, 'album_id')
    assert isinstance(valid_song.album_id, int)
    assert valid_song.album_id is not None
    q = Album.query.filter_by(id=valid_song.album_id).first()
    assert q.id is not None

def test_song_relations():
    pass


def test_create_song(valid_song):
    assert valid_song.name == 'TestName'
    assert valid_song.duration == datetime.time(0,3,48)
    assert valid_song.album_id == None
    db.session.add(valid_song)
    db.session.commit()
    assert valid_song.id is not None
    db.session.delete(valid_song)
    db.session.commit()


def test_get_song(valid_song):
    db.session.add(valid_song)
    db.session.commit()
    song = Song.query.filter_by(id=valid_song.id).first()
    assert song.name == 'TestName'
    assert song.duration == datetime.time(0,3,48)
    assert song.album_id == ''
    db.session.delete(valid_song)
    db.session.commit()


def test_update_song(valid_song):
    db.session.add(valid_song)
    db.session.commit()
    assert valid_song.id is not None
    song = db.session.query(Song).filter(Song.id == valid_song.id).first()
    song.name = 'NewName'
    song.duration = datetime.time(0, 2, 99)
    assert song.name == 'NewName'
    assert song.duration == datetime.time(0, 2, 99)
    db.session.delete(valid_song)
    db.session.commit()


def test_delete_song(invalid_song):
    db.session.add(invalid_song)
    db.session.commit()
    assert invalid_song.id is not None
    db.session.delete(invalid_song)
    db.session.commit()
    q = db.session.query(Song).filter(Song.id == invalid_song.id).first()
    assert q is None


def test_invalid_song(invalid_song):
    with pytest.raises(Exception):
        try:
            db.session.add(invalid_song)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

def test_valid_song(valid_song):
    db.session.add(valid_song)
    db.session.commit()
    assert valid_song.id is not None
    db.session.delete(valid_song)
    db.session.commit()



