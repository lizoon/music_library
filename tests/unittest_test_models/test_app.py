import os

from sqlalchemy.orm import sessionmaker
from app.models.user import User, Role

from app import app as _app
from app import db
import unittest

import flask_migrate
from flask_security import SQLAlchemyUserDatastore, Security


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.application = _app
        self.application.testing = True

        with self.application.app_context():
            db.engine.execute('DROP TABLE IF EXISTS {} CASCADE;'.format(', '.join(db.metadata.tables.keys())))
            db.engine.execute('DROP TABLE IF EXISTS alembic_version CASCADE;')
            # migrations_dir = '/home/liza/PycharmProjects/music_library/migrations'
            # flask_migrate.init(migrations_dir)
            flask_migrate.upgrade()
            self.db = db

        self.Session = sessionmaker(bind=self.db.engine)
        self.session = self.Session()

        self.user_datastore = SQLAlchemyUserDatastore(self.db, User, Role)
        # self.security = Security(self.application, self.user_datastore)

    def tearDown(self) -> None:
        self.session.close()




