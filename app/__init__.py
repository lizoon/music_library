import random

from flask import Flask, render_template, \
    abort, redirect, url_for, request, session, flash, Response
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, login_user, logout_user
from datetime import timedelta
from flask_bootstrap import Bootstrap

from flask_s3 import FlaskS3
import os
import shutil
import re
from flask_admin.contrib import sqla
from flask_admin import form

app = Flask(__name__, template_folder='templates')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

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


class StorageAdminModel(sqla.ModelView):
    form_extra_fields = {
        'file': form.FileUploadField('file', base_path=os.path.join(app.config["STORAGE"], "mp3"))
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                file = storage_file.filename
                ext = storage_file.filename.split('.')[-1]
                filename = file

                storage_file.save(
                    os.path.join(_form.file.base_path, filename)
                )

                # _form.name.data = _form.name.data or storage_file.filename
                _form.path.data = filename
                _form.type.data = ext
                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        result = super().edit_form(obj)
        return self._change_path_data(result)

    def create_form(self, obj=None):
        result = super().create_form(obj)
        return self._change_path_data(result)


class AlbumModel(sqla.ModelView):
    form_extra_fields = {
        'file': form.FileUploadField('file', base_path=os.path.join(app.config["STORAGE"], "img"))
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                file = storage_file.filename
                filename = file
                relative_path = os.path.join("img", filename)

                storage_file.save(os.path.join(app.config["STORAGE"], relative_path))

                _form.cover.data = relative_path
                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        result = super().edit_form(obj)
        return self._change_path_data(result)

    def create_form(self, obj=None):
        result = super().create_form(obj)
        return self._change_path_data(result)


admin = Admin(app, 'FlaskApp', url='/homepage', index_view=HomeAdminView(name='Home'), template_mode='bootstrap3')


bootstrap = Bootstrap(app)

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Artist, db.session))
admin.add_view(AdminView(Genre, db.session))
admin.add_view(AlbumModel(Album, db.session))
admin.add_view(StorageAdminModel(Song, db.session))


from app.controllers import album
from app.controllers import artist
from app.controllers import genre
from app.controllers import song
from app.controllers import user


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=40)

# Ac*GBPK.#P9pUAY
