from sqlalchemy.orm import relationship

from app import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Boolean, Sequence
from sqlalchemy.sql import text
from flask_security import UserMixin, RoleMixin


t_roles_users = Table(
    'roles_users', db.Model.metadata,
    Column('role_id', ForeignKey('roles.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = Column(Integer, Sequence("roles_id_seq"), primary_key=True)
    name = Column(String(15), nullable=False, unique=True)
    description = Column(String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, Sequence("users_id_seq"), primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    nickname = Column(String(20), nullable=False)
    active = Column(Boolean())

    roles = relationship('Role', secondary=t_roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User: {self.email}>'
