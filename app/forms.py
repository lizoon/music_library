from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Regexp


class LoginForm(FlaskForm):
    nickname = StringField('Nickname', validators=[InputRequired(message='The name must not be empty!'),
                                                   Length(min=1, max=20,
                                                          message='The length of the name must be between 4 and 15 characters!')])
    password = PasswordField('Password', validators=[InputRequired(message='The password must not be empty!'),
                                             Length(min=1,
                                                    message='The length of the password must be between 4 and 15 characters!')])
    remember = BooleanField('Remember me')


class SignUpForm(FlaskForm):
    email = StringField('Email',
                        validators=[Length(max=60, message='Mailbox too long! '),
                                    Email(message='Mail must be filled!'),
                                    Regexp('^[a-z A-Z 0-9 ]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                                           message='Invalid email!'), ])

    nickname = StringField('Nickname',
                           validators=[InputRequired(message='The name must not be empty!'),
                                       Length(min=1, max=20, message='The length of the name must be between 4 and 15 characters!'),
                                       Regexp('[a-z A-Z а-я А-Я 0-9]+', message='The name must contain letters!')])
    password = PasswordField('Password',
                             validators=[InputRequired(message='The password must not be empty!'),
                                         Length(min=1, message='The length of the password must be between 4 and 15 characters!')])


