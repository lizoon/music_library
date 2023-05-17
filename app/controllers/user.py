from flask_security import SQLAlchemyUserDatastore, Security, logout_user, login_user
from app.controllers.artist import *


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
