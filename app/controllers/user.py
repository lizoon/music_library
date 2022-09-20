from app import *
from app.models.user import *
from app.models.users_songs import *

from app.controllers.artist import *


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Regexp


class LoginForm(FlaskForm):
    nickname = StringField('Nickname', validators=[InputRequired(message='The name must not be empty!'),
                                                   Length(min=4, max=15,
                                                          message='The length of the name must be between 4 and 15 characters!')])
    password = PasswordField('Password', validators=[InputRequired(message='The password must not be empty!'),
                                             Length(min=4, max=10,
                                                    message='The length of the password must be between 4 and 15 characters!')])
    remember = BooleanField('Remember me')


class SignUp(FlaskForm):
    email = StringField('Email',
                        validators=[Length(max=30, message='Mailbox too long! '),
                                    Email(message='Mail must be filled!'),
                                    Regexp('^[a-z A-Z 0-9 ]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                                           message='Invalid email!'), ])

    nickname = StringField('Nickname',
                           validators=[InputRequired(message='The name must not be empty!'),
                                       Length(min=4, max=15, message='The length of the name must be between 4 and 15 characters!'),
                                       Regexp('[a-z A-Z а-я А-Я 0-9]+', message='The name must contain letters!')])
    password = PasswordField('Password',
                             validators=[InputRequired(message='The password must not be empty!'),
                                         Length(min=4, max=10, message='The length of the password must be between 4 and 15 characters!')])


@app.route('/')
def main():
    return render_template('main.html', title='Main page')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUp()

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    if form.validate_on_submit():
        user_datastore.create_user(password=form.password.data,
                                   email=form.email.data,
                                   nickname=form.nickname.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)


@app.route('/signup/homepage', methods=['POST', 'GET'])
@app.route('/login/homepage', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('homepage'))
    return render_template('sequrity/login_user.html', title='Log in', form=form)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html',
                           name=current_user.nickname,
                           user_id=current_user.id)


@app.route('/search')
@login_required
def search():
    q = request.args.get('q')
    if q:
        songs = db.session.query(Song).filter(Song.name.ilike(('%{0}%').format(q))).all()
        artists = db.session.query(Artist).filter(Artist.firstname.ilike(('%{0}%').format(q))
                                                  | Artist.surname.ilike(('%{0}%').format(q))).all()
        albums = db.session.query(Album).filter(Album.name.ilike(('%{0}%').format(q))).all()
        if albums != []:
            count = 0
            for a in albums:
                cover = (db.session.query(Album).filter(Album.name == a.name).with_entities(Album.cover).first())[0]
                a = [a, cover]
                albums[count] = a
                count += 1

        return render_template('search_res.html',
                               title='search',
                               songs=songs,
                               album=Album,
                               artist=Artist,
                               artists=artists,
                               albums=albums)
    else:
        genres = Genre.query.all()
        return render_template('search.html',
                               title='search',
                               user_id=current_user.id,
                               genres=genres)


@app.route('/library')
@login_required
def library():
    user_id = current_user.id
    songs = db.session.query(Song).filter(Song.users.any(User.id == user_id))
    return render_template('library.html',
                           title='library',
                           songs=songs,
                           album=Album,
                           artist=Artist)


# @app.route('/profile', methods=['POST', 'GET'])
# @login_required
# def profile():
#     songs = db.session.query(Song).filter(Song.users.any(User.id == current_user.id))
#     count = songs.count()
#     return render_template('profile.html',
#                            title='profile',
#                            user=current_user,
#                            count=count,
#                            songs=songs,
#                            album=Album,
#                            artist=Artist,
#                            func=fav_artist,
#                            flag=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/diagram')
@login_required
def diagram():
    user_id = current_user.id
    songs = db.session.query(Song).filter(Song.users.any(User.id == user_id))
    albums = []
    artists = []
    genres = []
    for song_ in songs:
        album_ = (db.session.query(Album).get(song_.album_id))
        albums.append(album_)

    for album_ in albums:
        artist_ = db.session.query(Artist).filter(Artist.id == album_.artist_id).first()
        artists.append(artist_)

    for artist_ in artists:
        genre_ = db.session.query(Genre).filter(Genre.id == artist_.genre_id).first()
        genres.append(genre_)

    data1 = {}
    data1.update({'Genre': 'Number of songs'})
    for genre_ in genres:
        count = genres.count(genre_)
        data1.update({genre_: count})

    return render_template('diagram.html',
                           title='diagram',
                           data1=data1)

