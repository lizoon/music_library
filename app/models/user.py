from app import db
from flask_security import UserMixin, RoleMixin

from sqlalchemy import Column, ForeignKey, Integer, Table, String, Boolean, text, CheckConstraint
from sqlalchemy.orm import relationship


t_roles_users = Table(
    'roles_users', db.Model.metadata,
    Column('role_id', ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, server_default=text("nextval('roles_id_seq')"))
    name = Column(String(15), nullable=False, unique=True)
    description = Column(String(255))


def get_all_users():
    return [User.json(user) for user in User.query.all()]


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = (CheckConstraint("regexp_like('^[a-z A-Z 0-9 ]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$')", name="email_check"),
                      CheckConstraint('(char_length((nickname)::text) >= 3) AND (char_length((nickname)::text) <= 15)', name='len_nickname'),
                      CheckConstraint('(char_length((password)::text) >= 3) AND (char_length((password)::text) <= 10)', name='len_password'),
                      )

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq')"))
    nickname = Column(String(20), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(60), nullable=False)
    active = Column(Boolean())

    roles = relationship('Role', secondary=t_roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'{self.nickname}'

    def json(self):
        return {'id': self.id,
                'nickname': self.nickname,
                'email': self.email,
                'password': self.password}

    def get_user(id_):
        return [User.json(db.session.query(User).filter(User.id == id_).first())]

    def add_user(nickname_, email_, password_, active_):
        new_user = User()
        new_user.nickname = nickname_
        new_user.email = email_
        new_user.password = password_
        new_user.active = active_
        db.session.add(new_user)
        db.session.commit()

    def update_user(id_, nickname_, email_, password_, active_):
        user_to_update = db.session.query(User).filter(User.id == id_).first()
        user_to_update.nickname = nickname_
        user_to_update.email = email_
        user_to_update.password = password_
        user_to_update.active = active_
        db.session.commit()

    def delete_user(id_):
        db.session.query(User).filter(User.id == id_).delete()
        db.session.commit()


