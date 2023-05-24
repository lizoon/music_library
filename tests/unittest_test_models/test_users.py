import unittest

from hamcrest import assert_that, matches_regexp, all_of, has_properties, contains_string, not_none
from sqlalchemy import insert

from app.models.song import Song
from app.models.user import User
from app.models.users_songs import t_users_songs
from tests.unittest_test_models.test_app import TestApp


class TestUser(TestApp):
    def test_user_attrs(self):
        valid_user = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)

        assert hasattr(valid_user, 'password')
        assert isinstance(valid_user.password, str)
        assert len(valid_user.password) >= 0

        assert hasattr(valid_user, 'email')
        assert isinstance(valid_user.email, str)
        assert 60 >= len(valid_user.email) >= 0
        query_result = self.session.query(User).filter_by(email=valid_user.email).count()
        assert query_result is not None

        assert_that(valid_user.email, matches_regexp(r'^[a-zA-Z0-9]+[._]?[a-z 0-9]+@\w+[.]\w{2,3}$'))

        assert hasattr(valid_user, 'nickname')
        assert isinstance(valid_user.nickname, str)
        assert 20 >= len(valid_user.nickname) >= 0

        assert hasattr(valid_user, 'active')
        assert isinstance(valid_user.active, bool)

    @unittest.skip("Skipping test_create_user")
    @unittest.expectedFailure
    def test_create_user(self, nickname, email, password):
        nickname = 'Test1'
        email = 'Test1@gmail.com'
        password = 'Test1'
        user = User(nickname=nickname, email=email, password=password)
        self.session.add(user)
        self.session.commit()
        self.assertEqual(user.password, nickname)
        self.assertEqual(user.email, email)
        self.assertEqual(user.nickname, password)
        self.assertFalse(user.is_anonymous)
        self.assertIsNotNone(user.id)

    def test_get_user(self):
        nickname = 'Test1'
        email = 'Test1@gmail.com'
        password = 'Test1'
        self.test_create_user(nickname, email, password)
        user = self.session.query(User).filter(User.email == email).first()
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.password)
        self.assertIsNotNone(user.nickname)
        self.assertIsNotNone(user.email)

    def test_update_user(self):
        nickname = 'Test1'
        email = 'Test1@gmail.com'
        password = 'Test1'
        self.test_create_user(nickname, email, password)
        user = self.session.query(User).filter(User.email == email).first()
        self.assertIsNotNone(user.id)
        user.password = 'new_password'
        user.email = 'new_email@gmail.com'
        user.nickname = 'new_nickname'
        self.session.commit()
        upd_user = self.session.query(User).filter(User.id == user.id).first()
        self.assertIsNotNone(upd_user.id)
        self.assertEqual(upd_user.password, 'new_password')
        self.assertEqual(upd_user.email, 'new_email@gmail.com')
        self.assertEqual(upd_user.nickname, 'new_nickname')

    def test_delete_user(self):
        nickname = 'Test1'
        email = 'Test1@gmail.com'
        password = 'Test1'
        self.test_create_user(nickname, email, password)
        user = self.session.query(User).filter(User.email == email).first()
        self.assertIsNotNone(user.id)
        self.session.delete(user)
        self.session.commit()
        q = self.session.query(User).filter(User.id == user.id).first()
        self.assertIsNone(q)

    def test_invalid_user(self):
        invalid_user = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)
        with self.assertRaises(Exception):
            try:
                self.session.add(invalid_user)
                self.session.commit()
            except Exception:
                self.session.rollback()
                raise

    def test_valid_user(self):
        valid_user = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)
        self.session.add(valid_user)
        self.session.commit()
        self.assertIsNotNone(valid_user.id)
        self.session.delete(valid_user)
        self.session.commit()

    def test_admin_user(self):
        user = self.user_datastore.create_user(password='admin', email='admin@gmail.com', nickname='admin', active=True)
        role = self.user_datastore.create_role(name='admin')
        self.user_datastore.add_role_to_user(user, role)
        self.user_datastore.commit()
        u = self.session.query(User).first()
        self.assertIsNotNone(u.id)
        self.assertEqual(u.password, 'admin')
        self.assertEqual(u.nickname, 'admin')
        self.assertEqual(u.email, 'admin@gmail.com')
        self.assertTrue(u.is_active)
        self.assertTrue(u.has_role('admin'))

    def test_many_admin_user(self):
        admins = [
            {'nickname': 'Admin1', 'email': 'Admin1@gmail.com', 'password': 'Admin1'},
            {'nickname': 'Admin2', 'email': 'Admin2@gmail.com', 'password': 'Admin2'},
            {'nickname': 'Admin3', 'email': 'Admin3@gmail.com', 'password': 'Admin3'}
        ]
        for admin in admins:
            user = User(password=admin['password'], email=admin['email'], nickname=admin['nickname'], active=True)
            role = Role(name='admin')
            self.session.add(user)
            self.session.add(role)
            self.session.commit()
            self.session.execute(insert(t_roles_users).values(user_id=user.id, role_id=role.id))

            assert_that(user, all_of(
                has_properties(
                    email=contains_string('@gmail.com'),
                    active=not_none(),
                    password=not_none(),
                    nickname=contains_string('Admin')
                ),
            ))

    def test_users_songs_relation(self):
        user = User(password='testtest', email='test2@gmail.com', nickname='test2', active=True)
        self.session.add(user)
        self.session.commit()
        song = self.session.query(Song).first()
        self.session.execute(insert(t_users_songs).values(user_id=user.id, song_id=song.id))
        self.session.commit()

        s = self.session.query(Song).get(song.id)
        self.assertEqual(s.users, [user])






