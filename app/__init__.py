from typing import Optional

from flask import Flask, redirect, url_for, request, session

from app.config import Configuration
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text, Table, Column,ForeignKey, PrimaryKeyConstraint, Integer, String, Boolean, CheckConstraint, Time, text,UniqueConstraint

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from datetime import timedelta

from flask_bootstrap import Bootstrap


def create_app(cfg: Optional[config.Configuration] = None) -> Flask:
    if cfg is None:
        cfg = config.Configuration()
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(cfg)

    db = create_db(application=app)
    db.init_app(app)
    return app


def create_db(application):
    db = SQLAlchemy(application)
    # migrate = Migrate(app, db)
    return db

app = create_app()
db = create_db(application=app)

from app.models.user import User, Role
from app.models.artist import Artist
from app.models.song import Song
from app.models.genre import Genre
from app.models.album import Album


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


# клас для ограничения админки вьюх
class AdminView(AdminMixin, ModelView):
    pass


# home view admin
class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('sequrity/index.html')


admin = Admin(app, 'FlaskApp', url='/homepage', index_view=HomeAdminView(name='Home'), template_mode='bootstrap3')
bootstrap = Bootstrap(app)


admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Artist, db.session))
admin.add_view(AdminView(Song, db.session))
admin.add_view(AdminView(Genre, db.session))
admin.add_view(AdminView(Album, db.session))


from app.controllers import album
from app.controllers import artist
from app.controllers import genre
from app.controllers import song
from app.controllers import user


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=40)

